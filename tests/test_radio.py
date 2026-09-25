import re
from typing import Any, Tuple
from unittest.mock import MagicMock

from yandex_music import Client, GenerativeStream, GenerativeStreamFeedback, Wave, WaveSettings


def _make_client(result: Any = 'ok') -> Tuple[Client, MagicMock]:
    post = MagicMock(return_value=result)
    client = Client()
    client._request = MagicMock(post=post)
    return client, post


def _make_get_client(result: Any) -> Tuple[Client, MagicMock]:
    get = MagicMock(return_value=result)
    client = Client()
    client._request = MagicMock(get=get)
    return client, get


class TestRadio:
    def test_rotor_station_feedback_sends_json_body(self):
        client, post = _make_client()

        result = client.rotor_station_feedback(
            'user:onyourwave',
            'trackFinished',
            timestamp='2024-01-01T12:00:00.000Z',
            from_='mobile-radio-user-onyourwave',
            batch_id='batch-1',
            total_played_seconds=42,
            track_id='12345:678',
        )

        assert result is True
        args, kwargs = post.call_args
        assert args[0] == 'https://api.music.yandex.net/rotor/station/user:onyourwave/feedback'
        assert 'data' not in kwargs
        assert kwargs['params'] == {'batch-id': 'batch-1'}
        assert kwargs['json'] == {
            'type': 'trackFinished',
            'timestamp': '2024-01-01T12:00:00.000Z',
            'trackId': '12345:678',
            'from': 'mobile-radio-user-onyourwave',
            'totalPlayedSeconds': 42,
        }

    def test_rotor_station_feedback_default_timestamp_is_utc_iso(self):
        client, post = _make_client()

        client.rotor_station_feedback('user:onyourwave', 'radioStarted')

        _, kwargs = post.call_args
        assert kwargs['params'] == {}
        # Числовое значение API трактует как миллисекунды, поэтому по умолчанию отправляется ISO 8601 в UTC
        assert re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z', kwargs['json']['timestamp'])

    def test_rotor_station_settings2_sends_json_body(self):
        client, post = _make_client()

        result = client.rotor_station_settings2('user:onyourwave', 'all', 'discover', 'any')

        assert result is True
        args, kwargs = post.call_args
        assert args[0] == 'https://api.music.yandex.net/rotor/station/user:onyourwave/settings3'
        assert 'data' not in kwargs
        assert kwargs['json'] == {'moodEnergy': 'all', 'diversity': 'discover', 'type': 'rotor', 'language': 'any'}

    def test_rotor_station_feedback_stream_id(self):
        client, post = _make_client()

        client.rotor_station_feedback('generative:focus', 'radioStarted', batch_id='batch-1', stream_id='stream-1')

        _, kwargs = post.call_args
        assert kwargs['params'] == {'batch-id': 'batch-1', 'streamId': 'stream-1'}

    def test_rotor_station_stream(self):
        client, get = _make_get_client({'version': '0.92', 'stream': {'id': 'stream-1', 'url': 'https://example.com'}})

        result = client.rotor_station_stream('generative:focus')

        assert isinstance(result, GenerativeStream)
        assert result.stream.id == 'stream-1'
        args, _ = get.call_args
        assert args[0] == 'https://api.music.yandex.net/rotor/station/generative:focus/stream'

    def test_rotor_station_stream_feedback(self):
        client, post = _make_client({'reload_stream': False, 'not_paused': True})

        result = client.rotor_station_stream_feedback(
            'generative:focus', 'streamPlay', 'stream-1', timestamp='2024-01-01T12:00:00.000Z'
        )

        assert isinstance(result, GenerativeStreamFeedback)
        assert result.not_paused is True
        args, kwargs = post.call_args
        assert args[0] == 'https://api.music.yandex.net/rotor/station/generative:focus/feedback'
        assert kwargs['params'] == {'streamId': 'stream-1'}
        assert kwargs['json'] == {'type': 'streamPlay', 'timestamp': '2024-01-01T12:00:00.000Z'}

    def test_rotor_wave_last(self):
        client, get = _make_get_client({'name': 'Моя волна', 'stationId': 'user:onyourwave'})

        result = client.rotor_wave_last()

        assert isinstance(result, Wave)
        assert result.station_id == 'user:onyourwave'
        args, _ = get.call_args
        assert args[0] == 'https://api.music.yandex.net/rotor/wave/last'

    def test_rotor_wave_last_reset(self):
        client, post = _make_client({'result': 'ok'})

        assert client.rotor_wave_last_reset() is True
        args, kwargs = post.call_args
        assert args[0] == 'https://api.music.yandex.net/rotor/wave/last/reset'
        assert 'json' not in kwargs

    def test_rotor_wave_settings_joins_seeds(self):
        client, get = _make_get_client({'blocks': []})

        result = client.rotor_wave_settings(['user:onyourwave', 'genre:rock'])

        assert isinstance(result, WaveSettings)
        args, _ = get.call_args
        assert args[0] == 'https://api.music.yandex.net/rotor/wave/settings'
        assert args[1] == {'seeds': 'user:onyourwave,genre:rock'}

    def test_rotor_wave_settings_without_seeds(self):
        client, get = _make_get_client({'blocks': []})

        client.rotor_wave_settings()

        args, _ = get.call_args
        assert args[1] == {}
