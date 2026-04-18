from unittest.mock import MagicMock

from yandex_music import Client, DeviceCode


def _make_client():
    client = Client()
    client._request = MagicMock()
    return client


class TestDeviceAuth:
    def test_request_device_code_returns_model(self):
        client = _make_client()
        client._request.post = MagicMock(
            return_value={
                'device_code': 'dev123',
                'user_code': 'USER01',
                'verification_url': 'https://oauth.yandex.ru/authorize/device',
                'expires_in': 300,
                'interval': 5,
            }
        )

        code = client.request_device_code()

        assert isinstance(code, DeviceCode)
        assert code.device_code == 'dev123'
        assert code.user_code == 'USER01'
        assert code.expires_in == 300
        assert code.interval == 5

    def test_request_device_code_sends_correct_payload(self):
        client = _make_client()
        client._request.post = MagicMock(
            return_value={
                'device_code': 'd',
                'user_code': 'u',
                'verification_url': 'https://x',
                'expires_in': 1,
                'interval': 1,
            }
        )

        client.request_device_code(device_id='my-id', device_name='my-name', client_id='my-cid')

        args, _ = client._request.post.call_args
        assert args[0] == 'https://oauth.yandex.ru/device/code'
        assert args[1] == {
            'client_id': 'my-cid',
            'device_id': 'my-id',
            'device_name': 'my-name',
        }

    def test_poll_device_token_returns_token(self):
        client = _make_client()
        client._request.post = MagicMock(
            return_value={
                'access_token': 'y0_tok',
                'refresh_token': '1:ref',
                'expires_in': 31536000,
                'token_type': 'bearer',
            }
        )

        from yandex_music import OAuthToken

        token = client.poll_device_token('dev123')

        assert isinstance(token, OAuthToken)
        assert token.access_token == 'y0_tok'
        assert token.refresh_token == '1:ref'

    def test_poll_device_token_pending_returns_none(self):
        from yandex_music.exceptions import BadRequestError

        client = _make_client()
        client._request.post = MagicMock(side_effect=BadRequestError('authorization_pending User code not confirmed'))

        assert client.poll_device_token('dev123') is None

    def test_poll_device_token_other_error_raises(self):
        import pytest

        from yandex_music.exceptions import BadRequestError, DeviceAuthError

        client = _make_client()
        client._request.post = MagicMock(side_effect=BadRequestError('expired_token Device code expired'))

        with pytest.raises(DeviceAuthError, match='expired_token'):
            client.poll_device_token('dev123')

    def test_poll_device_token_sends_correct_payload(self):
        client = _make_client()
        client._request.post = MagicMock(return_value={'access_token': 'tok'})

        client.poll_device_token('dev123', client_id='cid', client_secret='secret')

        args, _ = client._request.post.call_args
        assert args[0] == 'https://oauth.yandex.ru/token'
        assert args[1] == {
            'grant_type': 'device_code',
            'code': 'dev123',
            'client_id': 'cid',
            'client_secret': 'secret',
        }

    def test_device_auth_happy_path(self, monkeypatch):
        from yandex_music import OAuthToken

        client = _make_client()
        # First call (POST device/code), then two pending polls, then success
        post_mock = MagicMock()
        post_mock.side_effect = [
            {
                'device_code': 'dev123',
                'user_code': 'USR',
                'verification_url': 'https://x',
                'expires_in': 300,
                'interval': 5,
            },
        ]
        client._request.post = post_mock

        # Patch poll_device_token directly to simplify sequencing
        polls = [None, None, OAuthToken('y0_tok', 'ref', 31536000, 'bearer')]
        monkeypatch.setattr(client, 'poll_device_token', lambda *a, **kw: polls.pop(0))

        # Skip real sleeps
        monkeypatch.setattr('time.sleep', lambda *a, **kw: None)

        seen_code = {}

        def on_code(code):
            seen_code['code'] = code

        token = client.device_auth(on_code=on_code)

        assert isinstance(token, OAuthToken)
        assert token.access_token == 'y0_tok'
        assert seen_code['code'].user_code == 'USR'
        assert client.token == 'y0_tok'
        assert polls == []

    def test_device_auth_timeout(self, monkeypatch):
        import pytest

        from yandex_music.exceptions import DeviceAuthError

        client = _make_client()
        client._request.post = MagicMock(
            return_value={
                'device_code': 'd',
                'user_code': 'u',
                'verification_url': 'https://x',
                'expires_in': 10,
                'interval': 1,
            }
        )
        monkeypatch.setattr(client, 'poll_device_token', lambda *a, **kw: None)
        # Simulate time jumping past expires_in after the first check
        clock = iter([0.0, 0.0, 100.0, 200.0, 300.0])
        monkeypatch.setattr('time.monotonic', lambda: next(clock))
        monkeypatch.setattr('time.sleep', lambda *a, **kw: None)

        with pytest.raises(DeviceAuthError, match='timed out'):
            client.device_auth(on_code=lambda code: None)

    def test_device_auth_cancel(self, monkeypatch):
        import pytest

        from yandex_music.exceptions import DeviceAuthError

        client = _make_client()
        client._request.post = MagicMock(
            return_value={
                'device_code': 'd',
                'user_code': 'u',
                'verification_url': 'https://x',
                'expires_in': 300,
                'interval': 1,
            }
        )
        monkeypatch.setattr(client, 'poll_device_token', lambda *a, **kw: None)
        monkeypatch.setattr('time.sleep', lambda *a, **kw: None)

        calls = {'n': 0}

        def should_cancel():
            calls['n'] += 1
            return calls['n'] >= 3

        with pytest.raises(DeviceAuthError, match='cancelled'):
            client.device_auth(on_code=lambda code: None, should_cancel=should_cancel)
