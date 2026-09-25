import asyncio
import logging
import time
from typing import Any, Awaitable, Callable, List, Tuple

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
from yandex_music.ynison import _base, messages, simple_async
from yandex_music.ynison.client_async import YnisonClientAsync

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
)

WAIT_TIMEOUT = 5.0


@pytest.fixture(autouse=True)
def fast_backoff(monkeypatch):
    monkeypatch.setattr(_base, '_DEFAULT_BACKOFF_MS', [0, 10])
    monkeypatch.setattr(_base.random, 'uniform', lambda _a, _b: 0)


@pytest.fixture
def server():
    fake = FakeYnisonServer()
    yield fake
    fake.close()


def make_client(server: FakeYnisonServer, **kwargs: Any) -> YnisonClientAsync:
    # клиент создаётся вне event loop'а
    return server.patch_client(YnisonClientAsync('fake-token', device_id=CLIENT_DEVICE_ID, **kwargs))


def run(coro_fn: Callable[[], Awaitable[Any]]) -> Any:
    return asyncio.run(asyncio.wait_for(coro_fn(), timeout=15))


async def wait_until(predicate: Callable[[], bool], timeout: float = WAIT_TIMEOUT) -> None:
    deadline = time.monotonic() + timeout
    while not predicate():
        if time.monotonic() > deadline:
            raise AssertionError('Не дождались условия')
        await asyncio.sleep(0.005)


async def wait_received(server: FakeYnisonServer, key: str) -> Any:
    await wait_until(lambda: any(key in item for item in server.received))
    return next(item for item in server.received if key in item)


async def stop(client: YnisonClientAsync, task: 'asyncio.Future[None]') -> None:
    await client.disconnect()
    await asyncio.wait_for(task, timeout=WAIT_TIMEOUT)


class Recorder:
    """Собирает фреймы состояния и ошибки, пришедшие в listener'ы клиента."""

    def __init__(self, client: YnisonClientAsync) -> None:
        self.client = client
        self.states: List[int] = []
        self.errors: List[Tuple[YnisonError, Any]] = []
        client.on_state(self._on_state)
        client.on_error(self._on_error)

    async def _on_state(self, state: Any) -> None:
        await asyncio.sleep(0)
        self.states.append(state.timestamp_ms)

    def _on_error(self, error: YnisonError) -> None:
        latest = self.client.latest_state
        self.errors.append((error, latest.timestamp_ms if latest is not None else None))


class TestSession:
    def test_session_populates_state(self, server):
        client = make_client(server)

        async def main():
            async with client.session(timeout=5) as session_client:
                assert session_client is client
                assert client.is_running
                assert client.state.timestamp_ms == 1
                assert client.current_playable is not None
                assert client.current_playable.playable_id == '1000'
                assert client.active_device is not None
                assert client.active_device.info.device_id == PLAYER_DEVICE_ID
            assert not client.is_running

        run(main)

        assert server.redirect_count == 1
        assert server.state_count == 1
        assert server.received[0]['updateFullState']['device']['info']['deviceId'] == CLIENT_DEVICE_ID
        assert 'fake-ticket' in server.subprotocol_headers[1]

    def test_unauthorized_redirect_frame(self, server):
        server.redirect_frames = [UNAUTHORIZED_FRAME]
        client = make_client(server)

        async def main():
            async with client.session(timeout=10):
                pass

        started = time.monotonic()
        with pytest.raises(YnisonUnauthorizedError) as exc_info:
            run(main)

        assert time.monotonic() - started < 2
        assert exc_info.value.http_code == 401
        assert server.state_count == 0
        assert not client.is_running

    def test_unauthorized_redirect_frame_connect(self, server):
        server.redirect_frames = [UNAUTHORIZED_FRAME]
        client = make_client(server)
        recorder = Recorder(client)

        with pytest.raises(YnisonUnauthorizedError):
            run(client.connect)

        assert recorder.errors == []
        assert server.redirect_count == 1
        assert not client.is_running

    def test_unauthorized_http_status(self, server):
        server.reject_http_status = 403
        client = make_client(server)

        async def main():
            async with client.session(timeout=10):
                pass

        with pytest.raises(YnisonUnauthorizedError):
            run(main)

        assert server.redirect_count == 1

    def test_timeout(self, server, monkeypatch):
        monkeypatch.setattr(_base, '_DEFAULT_BACKOFF_MS', [5000])
        server.default_state_script = send_frames_then_close()
        client = make_client(server)

        async def main():
            async with client.session(timeout=0.3):
                pass

        started = time.monotonic()
        with pytest.raises(YnisonTimeoutError):
            run(main)

        assert time.monotonic() - started < 4
        assert not client.is_running

    def test_reuse(self, server):
        client = make_client(server)

        async def main():
            for seq in (1, 2, 3):
                server.state_json = make_state(seq=seq).to_json()
                async with client.session(timeout=5):
                    assert client.state.timestamp_ms == seq
                assert not client.is_running

        run(main)

        assert client._state_listeners == []
        assert client._error_listeners == []
        assert server.redirect_count == 3

    def test_reuse_across_event_loops(self, server):
        client = make_client(server)

        async def main():
            async with client.session(timeout=5):
                assert client.latest_state is not None

        run(main)
        run(main)

        assert server.redirect_count == 2
        assert client._state_listeners == []

    def test_connect_while_running(self, server):
        client = make_client(server)

        async def main():
            async with client.session(timeout=5):
                with pytest.raises(YnisonError, match='уже подключён'):
                    await client.connect()
                with pytest.raises(YnisonError, match='уже подключён'):
                    async with client.session():
                        pass
                assert client.is_running
                assert client.latest_state is not None

        run(main)

    def test_simple_get_state(self, server, monkeypatch):
        monkeypatch.setattr(YnisonClientAsync, '_redirect_uri', lambda _self: server.redirect_uri)
        monkeypatch.setattr(YnisonClientAsync, '_state_uri', lambda _self, redirect: f'ws://{redirect.host}/state')

        state = asyncio.run(simple_async.get_state('fake-token', device_id=CLIENT_DEVICE_ID, timeout=5))
        track = asyncio.run(simple_async.get_current_track('fake-token', device_id=CLIENT_DEVICE_ID, timeout=5))

        assert state.timestamp_ms == 1
        assert track is not None
        assert track.playable_id == '1000'


class TestReconnect:
    def test_state_error_frame(self, server):
        server.state_scripts = [send_frames_then_close(make_state(seq=1).to_json(), BAD_REQUEST_FRAME)]
        server.state_json = make_state(seq=2).to_json()
        client = make_client(server)
        recorder = Recorder(client)

        async def main():
            task = asyncio.ensure_future(client.connect())
            await wait_until(lambda: 2 in recorder.states)
            await stop(client, task)

        run(main)

        assert recorder.states == [1, 2]
        server_error, latest_at_error = recorder.errors[0]
        assert type(server_error) is YnisonServerError
        assert server_error.error_code == '400030002'
        assert latest_at_error == 1
        assert isinstance(recorder.errors[1][0], YnisonConnectionClosedError)
        assert len(recorder.errors) == 2
        assert server.redirect_count == 2

    def test_displaced(self, server):
        server.state_scripts = [send_frames_then_wait(make_state(seq=1).to_json(), DISPLACED_FRAME)]
        client = make_client(server)
        recorder = Recorder(client)

        with pytest.raises(YnisonDeviceDisplacedError) as exc_info:
            run(client.connect)

        assert exc_info.value.go_away_seconds == 3600
        assert recorder.states == [1]
        assert recorder.errors == []
        assert server.redirect_count == 1
        assert not client.is_running

    def test_displaced_inside_session(self, server):
        server.state_scripts = [send_frames_then_wait(make_state(seq=1).to_json())]
        client = make_client(server)

        async def main():
            async with client.session(timeout=5):
                await asyncio.to_thread(server.push, DISPLACED_FRAME)
                await wait_until(lambda: not client.is_running)

                with pytest.raises(YnisonConnectionClosedError) as exc_info:
                    await client.next_track()
                assert isinstance(exc_info.value.__cause__, YnisonDeviceDisplacedError)

        run(main)

        assert server.redirect_count == 1

    def test_server_closes_without_error(self, server):
        server.state_scripts = [send_frames_then_close(make_state(seq=1).to_json())]
        server.state_json = make_state(seq=2).to_json()
        client = make_client(server)
        recorder = Recorder(client)

        async def main():
            task = asyncio.ensure_future(client.connect())
            await wait_until(lambda: 2 in recorder.states)
            await stop(client, task)

        run(main)

        assert [type(error) for error, _ in recorder.errors] == [YnisonConnectionClosedError]
        assert recorder.errors[0][1] == 1
        assert server.redirect_count == 2

    def test_max_reconnect_attempts(self, server):
        server.default_state_script = send_frames_then_close()
        client = make_client(server, max_reconnect_attempts=2)
        recorder = Recorder(client)

        with pytest.raises(YnisonConnectionClosedError):
            run(client.connect)

        assert len(recorder.errors) == 3
        assert server.redirect_count == 3
        assert not client.is_running

    def test_max_reconnect_attempts_session(self, server):
        server.default_state_script = send_frames_then_close()
        client = make_client(server, max_reconnect_attempts=1)

        async def main():
            async with client.session(timeout=5):
                pass

        with pytest.raises(YnisonConnectionClosedError):
            run(main)

        assert server.redirect_count == 2

    def test_disconnect_during_backoff(self, server, monkeypatch):
        monkeypatch.setattr(_base, '_DEFAULT_BACKOFF_MS', [5000])
        server.default_state_script = send_frames_then_close()
        client = make_client(server)
        recorder = Recorder(client)

        async def main():
            task = asyncio.ensure_future(client.connect())
            await wait_until(lambda: len(recorder.errors) == 1)
            started = time.monotonic()
            await stop(client, task)
            return time.monotonic() - started

        assert run(main) < 1
        assert server.redirect_count == 1
        assert not client.is_running

    def test_disconnect_is_idempotent(self, server):
        client = make_client(server)

        async def main():
            await client.disconnect()
            task = asyncio.ensure_future(client.connect())
            await wait_until(lambda: client.latest_state is not None)
            await stop(client, task)
            await client.disconnect()

        run(main)


class TestCommands:
    def test_send_without_connection(self, server):
        client = make_client(server)

        async def main():
            with pytest.raises(YnisonConnectionClosedError):
                await client.send(messages.build_full_state_request(CLIENT_DEVICE_ID))

            async with client.session(timeout=5):
                pass

            with pytest.raises(YnisonConnectionClosedError):
                await client.pause()

        run(main)

    def test_no_active_device(self, server):
        server.state_json = make_state(active=False).to_json()
        client = make_client(server)

        async def main():
            async with client.session(timeout=5):
                assert client.active_device is None
                with pytest.raises(YnisonNoActiveDeviceError):
                    await client.pause()
                with pytest.raises(YnisonNoActiveDeviceError):
                    await client.resume()
                with pytest.raises(YnisonNoActiveDeviceError):
                    await client.set_volume(0.5)

        run(main)

        assert len(server.received) == 1

    def test_pause(self, server):
        server.state_json = make_state(
            status=make_playing_status(progress_ms=1000, paused=False, timestamp_ms=messages.get_timestamp())
        ).to_json()
        client = make_client(server)

        async def main():
            async with client.session(timeout=5):
                await client.pause()
                return await wait_received(server, 'updatePlayingStatus')

        status = run(main)['updatePlayingStatus']['playingStatus']

        assert status['paused'] is True
        assert int(status['progressMs']) >= 1000
        assert status['version']['deviceId'] == CLIENT_DEVICE_ID

    def test_next_and_previous_track(self, server):
        client = make_client(server)

        async def main():
            async with client.session(timeout=5):
                with pytest.raises(YnisonQueueBoundaryError):
                    await client.previous_track()
                await client.next_track()
                return await wait_received(server, 'updatePlayerState')

        queue = run(main)['updatePlayerState']['playerState']['playerQueue']

        assert queue['currentPlayableIndex'] == 1
        assert queue['entityId'] == 'fake-entity'

    def test_set_volume(self, server):
        client = make_client(server)

        async def main():
            async with client.session(timeout=5):
                await client.set_volume(-1)
                return await wait_received(server, 'updateVolumeInfo')

        request = run(main)['updateVolumeInfo']

        assert request['deviceId'] == PLAYER_DEVICE_ID
        # betterproto не сериализует громкость 0 (значение по умолчанию)
        assert request['volumeInfo'].get('volume', 0.0) == 0.0


class TestListeners:
    def test_listener_exception_is_logged(self, server, caplog):
        caplog.set_level(logging.ERROR, logger='yandex_music.ynison')
        client = make_client(server)

        @client.on_state
        def broken(_state):
            raise RuntimeError('listener failure')

        @client.on_state
        async def broken_async(_state):
            raise RuntimeError('async listener failure')

        recorder = Recorder(client)

        async def main():
            async with client.session(timeout=5):
                await client.pause()
                # сервер отвечает состоянием на каждый запрос, значит receive-loop жив
                await wait_until(lambda: len(recorder.states) >= 2)

        run(main)

        assert 'исключение в state listener' in caplog.text
        assert 'listener failure' in caplog.text
        assert 'async listener failure' in caplog.text

    def test_error_listener_exception_is_logged(self, server, caplog):
        caplog.set_level(logging.ERROR, logger='yandex_music.ynison')
        server.state_scripts = [send_frames_then_wait(make_state(seq=1).to_json(), BAD_REQUEST_FRAME)]
        client = make_client(server)
        received: List[YnisonError] = []

        @client.on_error
        async def broken(_error):
            raise RuntimeError('error listener failure')

        client.on_error(received.append)

        async def main():
            async with client.session(timeout=5):
                await wait_until(lambda: len(received) == 1)
                assert client.state.timestamp_ms == 1

        run(main)

        assert 'исключение в error listener' in caplog.text

    def test_async_listener_accepted(self, server):
        client = make_client(server)
        recorder = Recorder(client)

        async def main():
            async with client.session(timeout=5):
                pass

        run(main)

        assert recorder.states == [1]

    def test_remove_bound_method_listener(self, server):
        client = make_client(server)
        recorder = Recorder(client)
        client.remove_listener(recorder._on_state)
        client.remove_listener(recorder._on_error)

        assert client._state_listeners == []
        assert client._error_listeners == []
