import json

import pytest

pytest.importorskip('betterproto')
pytest.importorskip('websockets')

from websockets.datastructures import Headers
from websockets.exceptions import InvalidStatus
from websockets.http11 import Response

from yandex_music.exceptions import (
    YnisonConnectionClosedError,
    YnisonDeviceDisplacedError,
    YnisonError,
    YnisonNoActiveDeviceError,
    YnisonServerError,
    YnisonUnauthorizedError,
)
from yandex_music.ynison import _base
from yandex_music.ynison._base import is_terminal_error, parse_server_error
from yandex_music.ynison.client import YnisonClient
from yandex_music.ynison.models.ynison_redirect import RedirectResponse

from .ynison_fake_server import (
    BAD_REQUEST_FRAME,
    CLIENT_DEVICE_ID,
    DISPLACED_FRAME,
    UNAUTHORIZED_FRAME,
    make_state,
)


def _error_payload(frame: str) -> dict:
    return json.loads(frame)['error']


class TestParseServerError:
    def test_unauthorized_with_extra_headers(self):
        error = parse_server_error(_error_payload(UNAUTHORIZED_FRAME))

        assert type(error) is YnisonUnauthorizedError
        assert error.grpc_code == 16
        assert error.http_code == 401
        assert error.error_code == '400160000'
        assert error.backoff_ms == [0, 1000, 5000, 30000]
        assert error.go_away_seconds is None
        assert error.message.startswith('UNAUTHENTICATED')
        assert str(error) == error.message

    def test_bad_request_with_details(self):
        error = parse_server_error(_error_payload(BAD_REQUEST_FRAME))

        assert type(error) is YnisonServerError
        assert error.grpc_code == 3
        assert error.http_code == 400
        assert error.error_code == '400030002'
        assert error.backoff_ms == [0, 1000, 5000, 30000]
        assert error.go_away_seconds is None
        assert 'PARAMETERS_NOT_SET' in error.message

    def test_displaced(self):
        error = parse_server_error(_error_payload(DISPLACED_FRAME))

        assert type(error) is YnisonDeviceDisplacedError
        assert error.grpc_code == 9
        assert error.http_code == 400
        assert error.error_code == '400090001'
        assert error.go_away_seconds == 3600
        assert error.backoff_ms == [0, 1000, 5000, 30000]

    @pytest.mark.parametrize(
        'payload',
        [
            {'grpc_code': 7, 'message': 'denied'},
            {'http_code': 403, 'message': 'forbidden'},
            {'http_code': '401'},
            {'grpc_code': '16'},
        ],
    )
    def test_unauthorized_variants(self, payload):
        assert type(parse_server_error(payload)) is YnisonUnauthorizedError

    def test_empty_payload(self):
        error = parse_server_error({})

        assert type(error) is YnisonServerError
        assert error.message
        assert error.grpc_code is None
        assert error.http_code is None
        assert error.error_code is None
        assert error.backoff_ms == []
        assert error.go_away_seconds is None

    def test_garbage_values(self):
        error = parse_server_error(
            {
                'grpc_code': 'abc',
                'http_code': None,
                'details': {'ynison-backoff-millis': '0:x:500:', 'ynison-go-away-for-seconds': 'soon'},
            }
        )

        assert error.grpc_code is None
        assert error.http_code is None
        assert error.backoff_ms == [0, 500]
        assert error.go_away_seconds is None

    def test_details_not_dict(self):
        error = parse_server_error({'message': 'x', 'details': 'oops'})

        assert error.error_code is None
        assert error.backoff_ms == []

    def test_backoff_not_string(self):
        assert parse_server_error({'details': {'ynison-backoff-millis': 1000}}).backoff_ms == []


class TestIsTerminalError:
    def test_terminal(self):
        assert is_terminal_error(YnisonUnauthorizedError('x'))
        assert is_terminal_error(YnisonDeviceDisplacedError('x'))
        assert is_terminal_error(YnisonServerError('x', go_away_seconds=60))

    def test_not_terminal(self):
        assert not is_terminal_error(YnisonServerError('x'))
        assert not is_terminal_error(YnisonServerError('x', go_away_seconds=0))
        assert not is_terminal_error(YnisonConnectionClosedError('x'))
        assert not is_terminal_error(YnisonError('x'))

    def test_hierarchy(self):
        assert issubclass(YnisonUnauthorizedError, YnisonServerError)
        assert issubclass(YnisonDeviceDisplacedError, YnisonServerError)
        assert issubclass(YnisonServerError, YnisonError)


class TestBaseFrameParsing:
    def test_state_frame(self):
        client = YnisonClient('fake-token', device_id=CLIENT_DEVICE_ID)
        client._reconnect_attempt = 3

        state = client._parse_state_frame(make_state(seq=7).to_json())

        assert client.latest_state is state
        assert client.state.timestamp_ms == 7
        assert client._reconnect_attempt == 0

    def test_error_frame_does_not_overwrite_state(self):
        client = YnisonClient('fake-token', device_id=CLIENT_DEVICE_ID)
        state = client._parse_state_frame(make_state(seq=1).to_json())

        with pytest.raises(YnisonServerError) as exc_info:
            client._parse_state_frame(BAD_REQUEST_FRAME)

        assert exc_info.value.error_code == '400030002'
        assert client.latest_state is state

    @pytest.mark.parametrize('frame', ['not json', '[1, 2]', '"string"', 'null'])
    def test_invalid_frames(self, frame):
        client = YnisonClient('fake-token', device_id=CLIENT_DEVICE_ID)

        with pytest.raises(YnisonError):
            client._parse_state_frame(frame)
        assert client.latest_state is None

    def test_redirect_frame(self):
        client = YnisonClient('fake-token', device_id=CLIENT_DEVICE_ID)
        frame = RedirectResponse(host='example.invalid', redirect_ticket='ticket', session_id=5).to_json()

        redirect = client._parse_redirect_frame(frame)

        assert redirect.host == 'example.invalid'
        assert redirect.redirect_ticket == 'ticket'
        assert redirect.session_id == 5
        assert client._state_uri(redirect) == f'wss://example.invalid/{client._STATE_SERVICE}'
        # keep-alive не прислан, берутся дефолты
        assert client._ping_params(redirect) == (_base._DEFAULT_PING_INTERVAL, _base._DEFAULT_PING_TIMEOUT)

    def test_redirect_error_frame(self):
        client = YnisonClient('fake-token', device_id=CLIENT_DEVICE_ID)

        with pytest.raises(YnisonUnauthorizedError):
            client._parse_redirect_frame(UNAUTHORIZED_FRAME)

    def test_incomplete_redirect(self):
        client = YnisonClient('fake-token', device_id=CLIENT_DEVICE_ID)

        with pytest.raises(YnisonError, match='Неполный'):
            client._parse_redirect_frame(json.dumps({'host': 'example.invalid'}))


class TestReconnectPolicy:
    def test_schedule_and_limit(self, monkeypatch):
        monkeypatch.setattr(_base.random, 'uniform', lambda _a, _b: 0)
        client = YnisonClient('fake-token', device_id=CLIENT_DEVICE_ID, max_reconnect_attempts=5)
        last_error = YnisonConnectionClosedError('lost')
        client._remember_error(last_error)

        delays = [client._next_reconnect_delay() for _ in range(5)]

        # лестница по умолчанию, последняя ступень повторяется
        assert delays == [0.0, 1.0, 5.0, 30.0, 30.0]
        with pytest.raises(YnisonConnectionClosedError) as exc_info:
            client._next_reconnect_delay()
        assert exc_info.value is last_error

    def test_limit_without_error(self):
        client = YnisonClient('fake-token', device_id=CLIENT_DEVICE_ID, max_reconnect_attempts=0)

        with pytest.raises(YnisonError):
            client._next_reconnect_delay()

    def test_jitter(self):
        client = YnisonClient('fake-token', device_id=CLIENT_DEVICE_ID)

        delay = client._next_reconnect_delay()

        assert 0 <= delay <= 0.25

    def test_server_backoff_overrides_default(self, monkeypatch):
        monkeypatch.setattr(_base.random, 'uniform', lambda _a, _b: 0)
        client = YnisonClient('fake-token', device_id=CLIENT_DEVICE_ID)

        client._remember_error(YnisonServerError('x', backoff_ms=[100, 200]))

        assert [client._next_reconnect_delay() for _ in range(3)] == [0.1, 0.2, 0.2]

        client._parse_state_frame(make_state().to_json())
        client._reset_connection_state()
        assert client.latest_state is None
        assert client._backoff_ms == _base._DEFAULT_BACKOFF_MS
        assert client._reconnect_attempt == 0
        assert client._last_error is None

    def test_to_reconnectable_error(self):
        client = YnisonClient('fake-token', device_id=CLIENT_DEVICE_ID)
        displaced = YnisonDeviceDisplacedError('x')
        server_error = YnisonServerError('x')

        assert client._to_reconnectable_error(server_error) is server_error
        assert client._last_error is None

        closed = client._to_reconnectable_error(OSError('boom'))
        assert isinstance(closed, YnisonConnectionClosedError)
        assert isinstance(closed.__cause__, OSError)

        with pytest.raises(YnisonDeviceDisplacedError):
            client._to_reconnectable_error(displaced)
        # терминальная ошибка запоминается и становится причиной ошибки send()
        assert client._last_error is displaced
        no_connection = client._no_connection_error()
        assert isinstance(no_connection, YnisonConnectionClosedError)
        assert no_connection.__cause__ is displaced

    def test_no_connection_error_without_terminal(self):
        client = YnisonClient('fake-token', device_id=CLIENT_DEVICE_ID)
        client._last_error = YnisonConnectionClosedError('lost')

        assert client._no_connection_error().__cause__ is None

    @pytest.mark.parametrize('status', [401, 403])
    def test_http_auth_failure_is_terminal(self, status):
        exc = InvalidStatus(Response(status, 'Unauthorized', Headers()))

        client = YnisonClient('fake-token', device_id=CLIENT_DEVICE_ID)

        with pytest.raises(YnisonUnauthorizedError):
            client._to_reconnectable_error(exc)

    def test_http_other_status_is_reconnectable(self):
        exc = InvalidStatus(Response(502, 'Bad Gateway', Headers()))

        client = YnisonClient('fake-token', device_id=CLIENT_DEVICE_ID)

        assert isinstance(client._to_reconnectable_error(exc), YnisonConnectionClosedError)


class TestBaseMisc:
    def test_default_device_id_derived_from_token(self):
        first = YnisonClient('fake-token-a')

        assert first.device_id == YnisonClient('fake-token-a').device_id
        assert first.device_id != YnisonClient('fake-token-b').device_id
        assert len(first.device_id) == 12

    def test_state_before_first_frame(self):
        client = YnisonClient('fake-token', device_id=CLIENT_DEVICE_ID)

        assert client.latest_state is None
        assert client.current_playable is None
        assert client.active_device is None
        assert client.is_running is False
        with pytest.raises(YnisonError):
            _ = client.state

    def test_subprotocols_and_headers(self):
        client = YnisonClient('fake-token', device_id=CLIENT_DEVICE_ID, device_title='Remote')

        plain = client._get_subprotocols()
        redirected = client._get_subprotocols(RedirectResponse(host='h', redirect_ticket='tkt', session_id=42))

        assert plain[:2] == ['Bearer', 'v2']
        assert CLIENT_DEVICE_ID in plain[2]
        assert 'Remote' in plain[2]
        assert 'tkt' not in plain[2]
        assert 'tkt' in redirected[2]
        assert '42' in redirected[2]
        assert client._get_headers()['Authorization'] == 'OAuth fake-token'

    def test_listeners(self):
        client = YnisonClient('fake-token', device_id=CLIENT_DEVICE_ID)

        def state_listener(_state):
            pass

        def error_listener(_error):
            pass

        assert client.on_state(state_listener) is state_listener
        assert client.on_error(error_listener) is error_listener
        assert client._state_listeners == [state_listener]
        assert client._error_listeners == [error_listener]

        client.remove_listener(state_listener)
        client.remove_listener(error_listener)
        client.remove_listener(error_listener)  # повторное удаление ничего не делает

        assert client._state_listeners == []
        assert client._error_listeners == []

    def test_commands_without_active_device(self):
        client = YnisonClient('fake-token', device_id=CLIENT_DEVICE_ID)
        client._parse_state_frame(make_state(active=False).to_json())

        with pytest.raises(YnisonNoActiveDeviceError):
            client._build_set_paused_request(paused=True)
        with pytest.raises(YnisonNoActiveDeviceError):
            client._build_set_volume_request(0.5, None)
        with pytest.raises(YnisonNoActiveDeviceError):
            client._build_set_volume_request(0.5, CLIENT_DEVICE_ID)

        request = client._build_set_volume_request(0.5, 'otherdevice1')
        assert request.update_volume_info.device_id == 'otherdevice1'
