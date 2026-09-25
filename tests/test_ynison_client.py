import logging
import threading
import time
from typing import Any, Dict, List, Tuple

import pytest

pytest.importorskip('betterproto')
pytest.importorskip('websockets')

from yandex_music.exceptions import (
    YnisonConnectionClosedError,
    YnisonDeviceDisplacedError,
    YnisonError,
    YnisonNoActiveDeviceError,
    YnisonQueueBoundaryError,
    YnisonServerError,
    YnisonTimeoutError,
    YnisonUnauthorizedError,
)
from yandex_music.ynison import _base, messages
from yandex_music.ynison.client import YnisonClient

from .ynison_fake_server import (
    BAD_REQUEST_FRAME,
    CLIENT_DEVICE_ID,
    DISPLACED_FRAME,
    PLAYER_DEVICE_ID,
    UNAUTHORIZED_FRAME,
    FakeYnisonServer,
    make_playing_status,
    make_state,
    send_frames_then_close,
    send_frames_then_wait,
    wait_until,
)

JOIN_TIMEOUT = 5.0


@pytest.fixture(autouse=True)
def fast_backoff(monkeypatch):
    monkeypatch.setattr(_base, '_DEFAULT_BACKOFF_MS', [0, 10])
    monkeypatch.setattr(_base.random, 'uniform', lambda _a, _b: 0)


@pytest.fixture
def server():
    fake = FakeYnisonServer()
    yield fake
    fake.close()


def make_client(server: FakeYnisonServer, **kwargs: Any) -> YnisonClient:
    return server.patch_client(YnisonClient('fake-token', device_id=CLIENT_DEVICE_ID, **kwargs))


class Recorder:
    """Собирает фреймы состояния и ошибки, пришедшие в listener'ы клиента."""

    def __init__(self, client: YnisonClient) -> None:
        self.client = client
        self.states: List[int] = []
        # (ошибка, timestamp_ms последнего состояния на момент ошибки)
        self.errors: List[Tuple[YnisonError, Any]] = []
        client.on_state(self._on_state)
        client.on_error(self._on_error)

    def _on_state(self, state: Any) -> None:
        self.states.append(state.timestamp_ms)

    def _on_error(self, error: YnisonError) -> None:
        latest = self.client.latest_state
        self.errors.append((error, latest.timestamp_ms if latest is not None else None))


def start_connect(client: YnisonClient) -> Tuple[threading.Thread, Dict[str, BaseException]]:
    result: Dict[str, BaseException] = {}

    def target() -> None:
        try:
            client.connect()
        except BaseException as e:  # noqa: BLE001
            result['error'] = e

    thread = threading.Thread(target=target, daemon=True)
    thread.start()
    return thread, result


def stop(client: YnisonClient, thread: threading.Thread) -> None:
    client.disconnect()
    thread.join(JOIN_TIMEOUT)
    assert not thread.is_alive()


class TestSession:
    def test_session_populates_state(self, server):
        client = make_client(server)

        with client.session(timeout=5) as session_client:
            assert session_client is client
            assert client.is_running
            assert client.latest_state is not None
            assert client.state.timestamp_ms == 1
            assert client.current_playable is not None
            assert client.current_playable.playable_id == '1000'
            assert client.active_device is not None
            assert client.active_device.info.device_id == PLAYER_DEVICE_ID

        assert not client.is_running
        assert server.redirect_count == 1
        assert server.state_count == 1

        full_state = server.received[0]['updateFullState']
        assert full_state['device']['info']['deviceId'] == CLIENT_DEVICE_ID
        # state-сокет открыт с тикетом из редиректа
        assert 'fake-ticket' in server.subprotocol_headers[1]
        assert 'fake-ticket' not in server.subprotocol_headers[0]

    def test_unauthorized_redirect_frame(self, server):
        server.redirect_frames = [UNAUTHORIZED_FRAME]
        client = make_client(server)

        started = time.monotonic()
        with pytest.raises(YnisonUnauthorizedError) as exc_info, client.session(timeout=10):
            pass

        assert time.monotonic() - started < 2
        assert exc_info.value.http_code == 401
        assert server.redirect_count == 1
        assert server.state_count == 0
        assert not client.is_running

    def test_unauthorized_redirect_frame_connect(self, server):
        server.redirect_frames = [UNAUTHORIZED_FRAME]
        client = make_client(server)
        recorder = Recorder(client)

        thread, result = start_connect(client)
        thread.join(JOIN_TIMEOUT)

        assert not thread.is_alive()
        assert isinstance(result.get('error'), YnisonUnauthorizedError)
        assert recorder.errors == []
        assert server.redirect_count == 1
        assert not client.is_running

    def test_unauthorized_http_status(self, server):
        server.reject_http_status = 401
        client = make_client(server)

        with pytest.raises(YnisonUnauthorizedError), client.session(timeout=10):
            pass

        assert server.redirect_count == 1

    def test_timeout(self, server, monkeypatch):
        monkeypatch.setattr(_base, '_DEFAULT_BACKOFF_MS', [5000])
        server.default_state_script = send_frames_then_close()
        client = make_client(server)

        started = time.monotonic()
        with pytest.raises(YnisonTimeoutError), client.session(timeout=0.3):
            pass

        assert time.monotonic() - started < 3
        assert not client.is_running

    def test_reuse(self, server):
        client = make_client(server)

        for seq in (1, 2, 3):
            server.state_json = make_state(seq=seq).to_json()
            with client.session(timeout=5):
                assert client.state.timestamp_ms == seq
            assert not client.is_running

        assert client._state_listeners == []
        assert client._error_listeners == []
        assert server.redirect_count == 3
        assert server.state_count == 3

    def test_connect_while_running(self, server):
        client = make_client(server)

        with client.session(timeout=5):
            with pytest.raises(YnisonError, match='уже подключён'):
                client.connect()
            with pytest.raises(YnisonError, match='уже подключён'), client.session():
                pass
            assert client.is_running
            assert client.latest_state is not None

    def test_on_state_async_listener_rejected(self, server):
        client = make_client(server)

        async def listener(_state):
            pass

        with pytest.raises(TypeError):
            client.on_state(listener)
        assert client._state_listeners == []


class TestReconnect:
    def test_state_error_frame(self, server):
        server.state_scripts = [send_frames_then_close(make_state(seq=1).to_json(), BAD_REQUEST_FRAME)]
        server.state_json = make_state(seq=2).to_json()
        client = make_client(server)
        recorder = Recorder(client)

        thread, result = start_connect(client)
        wait_until(lambda: 2 in recorder.states)
        stop(client, thread)

        assert 'error' not in result
        assert recorder.states == [1, 2]
        server_error, latest_at_error = recorder.errors[0]
        assert type(server_error) is YnisonServerError
        assert server_error.error_code == '400030002'
        # error-фрейм не затёр последнее состояние
        assert latest_at_error == 1
        assert isinstance(recorder.errors[1][0], YnisonConnectionClosedError)
        assert len(recorder.errors) == 2
        # переподключение снова прошло через редирект
        assert server.redirect_count == 2
        assert server.state_count == 2

    def test_state_error_frame_keeps_connection(self, server):
        # сервер прислал ошибку, но соединение не закрыл, клиент продолжает работу
        server.state_scripts = [send_frames_then_wait(make_state(seq=1).to_json(), BAD_REQUEST_FRAME)]
        client = make_client(server)
        recorder = Recorder(client)

        with client.session(timeout=5):
            wait_until(lambda: len(recorder.errors) == 1)
            assert client.state.timestamp_ms == 1
            client.pause()
            server.wait_received('updatePlayingStatus')

        assert server.redirect_count == 1

    def test_displaced(self, server):
        server.state_scripts = [send_frames_then_wait(make_state(seq=1).to_json(), DISPLACED_FRAME)]
        client = make_client(server)
        recorder = Recorder(client)

        thread, result = start_connect(client)
        thread.join(JOIN_TIMEOUT)

        assert not thread.is_alive()
        error = result.get('error')
        assert isinstance(error, YnisonDeviceDisplacedError)
        assert error.go_away_seconds == 3600
        assert recorder.states == [1]
        assert recorder.errors == []
        assert server.redirect_count == 1
        assert not client.is_running

    def test_displaced_inside_session(self, server):
        server.state_scripts = [send_frames_then_wait(make_state(seq=1).to_json())]
        client = make_client(server)

        with client.session(timeout=5):
            # сервер вытесняет устройство уже после выдачи состояния
            server.wait_for(lambda: server.state_count == 1)
            server.push(DISPLACED_FRAME)
            wait_until(lambda: not client.is_running)

            with pytest.raises(YnisonConnectionClosedError) as exc_info:
                client.next_track()
            assert isinstance(exc_info.value.__cause__, YnisonDeviceDisplacedError)

        assert server.redirect_count == 1

    def test_server_closes_without_error(self, server):
        server.state_scripts = [send_frames_then_close(make_state(seq=1).to_json())]
        server.state_json = make_state(seq=2).to_json()
        client = make_client(server)
        recorder = Recorder(client)

        thread, result = start_connect(client)
        wait_until(lambda: 2 in recorder.states)
        stop(client, thread)

        assert 'error' not in result
        assert [type(error) for error, _ in recorder.errors] == [YnisonConnectionClosedError]
        assert recorder.errors[0][1] == 1
        assert server.redirect_count == 2

    def test_max_reconnect_attempts(self, server):
        server.default_state_script = send_frames_then_close()
        client = make_client(server, max_reconnect_attempts=2)
        recorder = Recorder(client)

        thread, result = start_connect(client)
        thread.join(JOIN_TIMEOUT)

        assert not thread.is_alive()
        assert isinstance(result.get('error'), YnisonConnectionClosedError)
        assert len(recorder.errors) == 3
        assert server.redirect_count == 3
        assert not client.is_running

    def test_max_reconnect_attempts_session(self, server):
        server.default_state_script = send_frames_then_close()
        client = make_client(server, max_reconnect_attempts=1)

        with pytest.raises(YnisonConnectionClosedError), client.session(timeout=5):
            pass

        assert server.redirect_count == 2

    def test_successful_frame_resets_attempts(self, server):
        # каждое соединение отдаёт состояние и закрывается: счётчик сбрасывается, лимит не достигается
        server.default_state_script = send_frames_then_close(make_state(seq=1).to_json())
        client = make_client(server, max_reconnect_attempts=1)
        recorder = Recorder(client)

        thread, result = start_connect(client)
        wait_until(lambda: len(recorder.states) >= 4)
        stop(client, thread)

        assert 'error' not in result

    def test_disconnect_during_backoff(self, server, monkeypatch):
        monkeypatch.setattr(_base, '_DEFAULT_BACKOFF_MS', [5000])
        server.default_state_script = send_frames_then_close()
        client = make_client(server)
        recorder = Recorder(client)

        thread, result = start_connect(client)
        wait_until(lambda: len(recorder.errors) == 1)

        started = time.monotonic()
        stop(client, thread)

        assert time.monotonic() - started < 1
        assert 'error' not in result
        assert server.redirect_count == 1
        assert not client.is_running

    def test_disconnect_is_idempotent(self, server):
        client = make_client(server)
        client.disconnect()

        thread, _ = start_connect(client)
        wait_until(lambda: client.latest_state is not None)
        stop(client, thread)
        client.disconnect()


class TestCommands:
    def test_send_without_connection(self, server):
        client = make_client(server)

        with pytest.raises(YnisonConnectionClosedError):
            client.send(messages.build_full_state_request(CLIENT_DEVICE_ID))

        with client.session(timeout=5):
            pass

        with pytest.raises(YnisonConnectionClosedError):
            client.pause()

    def test_no_active_device(self, server):
        server.state_json = make_state(active=False).to_json()
        client = make_client(server)

        with client.session(timeout=5):
            assert client.active_device is None
            with pytest.raises(YnisonNoActiveDeviceError):
                client.pause()
            with pytest.raises(YnisonNoActiveDeviceError):
                client.resume()
            with pytest.raises(YnisonNoActiveDeviceError):
                client.set_volume(0.5)

        assert len(server.received) == 1

    def test_pause(self, server):
        server.state_json = make_state(
            status=make_playing_status(progress_ms=1000, paused=False, timestamp_ms=messages.get_timestamp())
        ).to_json()
        client = make_client(server)

        with client.session(timeout=5):
            client.pause()
            request = server.wait_received('updatePlayingStatus')

        status = request['updatePlayingStatus']['playingStatus']
        assert status['paused'] is True
        assert int(status['progressMs']) >= 1000
        assert status['version']['deviceId'] == CLIENT_DEVICE_ID

    def test_resume(self, server):
        client = make_client(server)

        with client.session(timeout=5):
            client.resume()
            request = server.wait_received('updatePlayingStatus')

        assert not request['updatePlayingStatus']['playingStatus'].get('paused', False)

    def test_next_and_previous_track(self, server):
        client = make_client(server)

        with client.session(timeout=5):
            with pytest.raises(YnisonQueueBoundaryError):
                client.previous_track()
            client.next_track()
            request = server.wait_received('updatePlayerState')

        queue = request['updatePlayerState']['playerState']['playerQueue']
        assert queue['currentPlayableIndex'] == 1
        assert queue['entityId'] == 'fake-entity'

    def test_set_volume(self, server):
        client = make_client(server)

        with client.session(timeout=5):
            client.set_volume(1.7)
            request = server.wait_received('updateVolumeInfo')

        assert request['updateVolumeInfo']['deviceId'] == PLAYER_DEVICE_ID
        assert request['updateVolumeInfo']['volumeInfo']['volume'] == 1.0


class TestListeners:
    def test_listener_exception_is_logged(self, server, caplog):
        caplog.set_level(logging.ERROR, logger='yandex_music.ynison')
        client = make_client(server)

        @client.on_state
        def broken(_state):
            raise RuntimeError('listener failure')

        @client.on_error
        def broken_error(_error):
            raise RuntimeError('error listener failure')

        recorder = Recorder(client)

        with client.session(timeout=5):
            client.pause()
            # сервер отвечает состоянием на каждый запрос, значит receive-loop жив
            wait_until(lambda: len(recorder.states) >= 2)

        assert 'исключение в state listener' in caplog.text
        assert 'listener failure' in caplog.text

    def test_error_listener_exception_is_logged(self, server, caplog):
        caplog.set_level(logging.ERROR, logger='yandex_music.ynison')
        server.state_scripts = [send_frames_then_wait(make_state(seq=1).to_json(), BAD_REQUEST_FRAME)]
        client = make_client(server)
        received: List[YnisonError] = []

        @client.on_error
        def broken(_error):
            raise RuntimeError('error listener failure')

        client.on_error(received.append)

        with client.session(timeout=5):
            wait_until(lambda: len(received) == 1)

        assert 'исключение в error listener' in caplog.text

    def test_remove_listener(self, server):
        client = make_client(server)
        recorder = Recorder(client)
        client.remove_listener(recorder._on_state)

        with client.session(timeout=5):
            pass

        assert recorder.states == []
