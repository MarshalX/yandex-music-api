"""Локальный фейковый сервер Ynison для тестов клиентов.

Сервер на `websockets.sync.server` крутится в фоновом потоке и обслуживает два пути:
`/redirect` (сервис редиректа, указывающий на самого себя) и `/state` (state-сервис).
Поведение каждого подключения можно заскриптовать очередями `redirect_frames` и `state_scripts`.
"""

import json
import threading
import time
from typing import Any, Callable, Dict, List, Optional

from websockets.exceptions import ConnectionClosed
from websockets.sync.server import ServerConnection, serve

from yandex_music.ynison.models import ynison_state
from yandex_music.ynison.models.ynison_redirect import KeepAliveParams, RedirectResponse

CLIENT_DEVICE_ID = '810eb13dbcd1'
PLAYER_DEVICE_ID = 'fakeplayer01'

UNAUTHORIZED_FRAME = json.dumps(
    {
        'error': {
            'grpc_code': 16,
            'http_code': 401,
            'message': 'UNAUTHENTICATED: fake',
            'extra_headers': {'ynison-error-code': '400160000', 'ynison-backoff-millis': '0:1000:5000:30000'},
        }
    }
)
BAD_REQUEST_FRAME = json.dumps(
    {
        'error': {
            'details': {'ynison-error-code': '400030002', 'ynison-backoff-millis': '0:1000:5000:30000'},
            'grpc_code': 3,
            'http_code': 400,
            'http_status': 'Bad Request',
            'message': "Unknown update request 'PARAMETERS_NOT_SET'",
        }
    }
)
DISPLACED_FRAME = json.dumps(
    {
        'error': {
            'details': {
                'ynison-error-code': '400090001',
                'ynison-go-away-for-seconds': '3600',
                'ynison-backoff-millis': '0:1000:5000:30000',
            },
            'grpc_code': 9,
            'http_code': 400,
            'http_status': 'Bad Request',
            'message': 'Current device has been dislocated by newly connected device with the same deviceId',
        }
    }
)


def make_playing_status(
    progress_ms: int = 1000,
    duration_ms: int = 200000,
    paused: bool = True,
    playback_speed: float = 1.0,
    timestamp_ms: int = 0,
) -> ynison_state.PlayingStatus:
    return ynison_state.PlayingStatus(
        progress_ms=progress_ms,
        duration_ms=duration_ms,
        paused=paused,
        playback_speed=playback_speed,
        version=ynison_state.UpdateVersion(device_id=PLAYER_DEVICE_ID, version=1, timestamp_ms=timestamp_ms),
    )


def make_queue(
    size: int = 3,
    current: int = 0,
    shuffle: Optional[List[int]] = None,
) -> ynison_state.PlayerQueue:
    queue = ynison_state.PlayerQueue(
        entity_id='fake-entity',
        entity_type=ynison_state.PlayerQueueEntityType.PLAYLIST,
        current_playable_index=current,
        playable_list=[
            ynison_state.Playable(
                playable_id=str(1000 + i),
                playable_type=ynison_state.PlayablePlayableType.TRACK,
                title=f'Track {i}',
            )
            for i in range(size)
        ],
        options=ynison_state.PlayerStateOptions(repeat_mode=ynison_state.PlayerStateOptionsRepeatMode.NONE),
        version=ynison_state.UpdateVersion(device_id=PLAYER_DEVICE_ID, version=1, timestamp_ms=1),
    )
    if shuffle is not None:
        queue.shuffle_optional = ynison_state.Shuffle(playable_indices=shuffle)
    return queue


def make_state(
    seq: int = 1,
    active: bool = True,
    queue: Optional[ynison_state.PlayerQueue] = None,
    status: Optional[ynison_state.PlayingStatus] = None,
) -> ynison_state.PutYnisonStateResponse:
    """Собирает фрейм состояния; `seq` кладётся в `timestamp_ms`, чтобы различать фреймы."""
    return ynison_state.PutYnisonStateResponse(
        player_state=ynison_state.PlayerState(
            status=status or make_playing_status(),
            player_queue=queue or make_queue(),
        ),
        devices=[
            ynison_state.Device(
                info=ynison_state.DeviceInfo(
                    device_id=PLAYER_DEVICE_ID,
                    title='Fake Player',
                    type=ynison_state.DeviceType.WEB,
                    app_name='fake',
                ),
                volume=0.5,
            )
        ],
        active_device_id_optional=PLAYER_DEVICE_ID if active else None,
        timestamp_ms=seq,
        rid=f'rid-{seq}',
    )


StateScript = Callable[[ServerConnection, 'FakeYnisonServer'], None]


class FakeYnisonServer:
    """Фейковый Ynison: редирект на себя и state-сервис со скриптуемым поведением."""

    def __init__(self) -> None:
        self.redirect_frames: List[str] = []
        self.state_scripts: List[StateScript] = []
        self.default_state_script: StateScript = serve_state_forever
        self.state_json: str = make_state(seq=1).to_json()
        self.reject_http_status: Optional[int] = None

        self.redirect_count = 0
        self.state_count = 0
        self.received: List[Dict[str, Any]] = []
        self.subprotocol_headers: List[str] = []

        self._cond = threading.Condition()
        self._connections: List[ServerConnection] = []
        self._state_connections: List[ServerConnection] = []
        self._server = serve(self._handler, '127.0.0.1', 0, process_request=self._process_request, close_timeout=0.1)
        self.port = self._server.socket.getsockname()[1]
        self._thread = threading.Thread(target=self._server.serve_forever, name='fake-ynison', daemon=True)
        self._thread.start()

    @property
    def redirect_uri(self) -> str:
        return f'ws://127.0.0.1:{self.port}/redirect'

    def redirect_json(self) -> str:
        return RedirectResponse(
            host=f'127.0.0.1:{self.port}',
            redirect_ticket='fake-ticket',
            session_id=123,
            keep_alive_params=KeepAliveParams(keep_alive_time_seconds=60, keep_alive_timeout_seconds=30),
        ).to_json()

    def patch_client(self, client: Any) -> Any:
        """Направляет клиента на этот сервер вместо настоящего Ynison."""
        client._redirect_uri = lambda: self.redirect_uri
        client._state_uri = lambda redirect: f'ws://{redirect.host}/state'
        return client

    def wait_for(self, predicate: Callable[[], bool], timeout: float = 5.0) -> None:
        with self._cond:
            if not self._cond.wait_for(predicate, timeout=timeout):
                raise AssertionError('Не дождались условия на фейковом сервере')

    def wait_received(self, key: str, timeout: float = 5.0) -> Dict[str, Any]:
        """Ждёт запрос с ключом `key` (например, `updatePlayingStatus`) и возвращает его."""

        def find() -> Optional[Dict[str, Any]]:
            return next((item for item in self.received if key in item), None)

        self.wait_for(lambda: find() is not None, timeout)
        result = find()
        assert result is not None
        return result

    def push(self, frame: str) -> None:
        """Отправляет фрейм в последнее state-соединение."""
        with self._cond:
            ws = self._state_connections[-1]
        ws.send(frame)

    def record(self, message: Any) -> None:
        with self._cond:
            self.received.append(json.loads(message))
            self._cond.notify_all()

    def _process_request(self, connection: ServerConnection, request: Any) -> Any:
        if self.reject_http_status is not None:
            with self._cond:
                self.redirect_count += 1
                self._cond.notify_all()
            return connection.respond(self.reject_http_status, 'Rejected\n')
        return None

    def _handler(self, ws: ServerConnection) -> None:
        with self._cond:
            self._connections.append(ws)
            self.subprotocol_headers.append(ws.request.headers.get('Sec-WebSocket-Protocol', ''))
        try:
            if ws.request.path == '/redirect':
                with self._cond:
                    self.redirect_count += 1
                    frame = self.redirect_frames.pop(0) if self.redirect_frames else self.redirect_json()
                    self._cond.notify_all()
                ws.send(frame)
                # сервис редиректа закрывает соединение сам
                ws.close()
            elif ws.request.path == '/state':
                with self._cond:
                    self.state_count += 1
                    self._state_connections.append(ws)
                    script = self.state_scripts.pop(0) if self.state_scripts else self.default_state_script
                    self._cond.notify_all()
                script(ws, self)
        except ConnectionClosed:
            pass

    def close(self) -> None:
        self._server.shutdown()
        with self._cond:
            connections = list(self._connections)
        for ws in connections:
            ws.close()
        self._thread.join(timeout=2)


def serve_state_forever(ws: ServerConnection, server: FakeYnisonServer) -> None:
    """Принимает full state, шлёт состояние и отвечает состоянием на каждый следующий запрос."""
    server.record(ws.recv())
    ws.send(server.state_json)
    for message in ws:
        server.record(message)
        ws.send(server.state_json)


def send_frames_then_close(*frames: str) -> StateScript:
    """Принимает full state, шлёт указанные фреймы и закрывает соединение."""

    def script(ws: ServerConnection, server: FakeYnisonServer) -> None:
        server.record(ws.recv())
        for frame in frames:
            ws.send(frame)
        ws.close()

    return script


def send_frames_then_wait(*frames: str) -> StateScript:
    """Принимает full state, шлёт фреймы и держит соединение, пока его не закроет клиент."""

    def script(ws: ServerConnection, server: FakeYnisonServer) -> None:
        server.record(ws.recv())
        for frame in frames:
            ws.send(frame)
        for message in ws:
            server.record(message)

    return script


def wait_until(predicate: Callable[[], bool], timeout: float = 5.0) -> None:
    deadline = time.monotonic() + timeout
    while not predicate():
        if time.monotonic() > deadline:
            raise AssertionError('Не дождались условия')
        time.sleep(0.005)
