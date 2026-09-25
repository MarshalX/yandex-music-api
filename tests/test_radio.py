from typing import Tuple
from unittest.mock import MagicMock

from yandex_music import Client


def _make_client() -> Tuple[Client, MagicMock]:
    post = MagicMock(return_value='ok')
    client = Client()
    client._request = MagicMock(post=post)
    return client, post


class TestRadio:
    def test_rotor_station_feedback_sends_json_body(self):
        client, post = _make_client()

        result = client.rotor_station_feedback(
            'user:onyourwave',
            'trackFinished',
            timestamp=1700000000.5,
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
            'timestamp': 1700000000.5,
            'trackId': '12345:678',
            'from': 'mobile-radio-user-onyourwave',
            'totalPlayedSeconds': 42,
        }

    def test_rotor_station_feedback_default_timestamp_is_number(self):
        client, post = _make_client()

        client.rotor_station_feedback('user:onyourwave', 'radioStarted')

        _, kwargs = post.call_args
        assert kwargs['params'] == {}
        assert isinstance(kwargs['json']['timestamp'], float)

    def test_rotor_station_settings2_sends_json_body(self):
        client, post = _make_client()

        result = client.rotor_station_settings2('user:onyourwave', 'all', 'discover', 'any')

        assert result is True
        args, kwargs = post.call_args
        assert args[0] == 'https://api.music.yandex.net/rotor/station/user:onyourwave/settings3'
        assert 'data' not in kwargs
        assert kwargs['json'] == {'moodEnergy': 'all', 'diversity': 'discover', 'type': 'rotor', 'language': 'any'}
