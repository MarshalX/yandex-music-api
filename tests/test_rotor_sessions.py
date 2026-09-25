import re
from typing import Any, Tuple
from unittest.mock import MagicMock

from yandex_music import (
    Client,
    CombinedSession,
    CombinedSessionLanding,
    CombinedSessionQueueItem,
    RotorSession,
    RotorSessionTracks,
    SessionEvent,
    SessionFeedback,
    SessionFeedbacks,
    SessionPlayable,
)

BASE = 'https://api.music.yandex.net/rotor'
ISO_UTC = r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z'


def _make_client(result: Any) -> Tuple[Client, MagicMock]:
    post = MagicMock(return_value=result)
    client = Client()
    client._request = MagicMock(post=post)
    return client, post


class TestRotorSessions:
    def test_rotor_session_new_minimal(self):
        client, post = _make_client({'radioSessionId': 'session-1', 'batchId': 'batch-1'})

        result = client.rotor_session_new('user:onyourwave')

        assert isinstance(result, RotorSession)
        assert result.radio_session_id == 'session-1'
        args, kwargs = post.call_args
        assert args[0] == f'{BASE}/session/new'
        assert kwargs['json'] == {'seeds': ['user:onyourwave']}

    def test_rotor_session_new_all(self):
        client, post = _make_client({})

        client.rotor_session_new(
            ['genre:rock', 'settingDiversity:discover'],
            queue=['12345:678'],
            track_to_start_from='12345',
            include_tracks_in_response=False,
            include_wave_model=True,
            interactive=True,
            incognito=True,
            child=False,
            allow_explicit=False,
        )

        _, kwargs = post.call_args
        assert kwargs['json'] == {
            'seeds': ['genre:rock', 'settingDiversity:discover'],
            'queue': ['12345:678'],
            'trackToStartFrom': '12345',
            'includeTracksInResponse': False,
            'includeWaveModel': True,
            'interactive': True,
            'incognito': True,
            'child': False,
            'allowExplicit': False,
        }

    def test_rotor_session_clone_sends_empty_json_body(self):
        client, post = _make_client({'radioSessionId': 'session-2'})

        result = client.rotor_session_clone('session-1')

        assert isinstance(result, RotorSession)
        args, kwargs = post.call_args
        assert args[0] == f'{BASE}/session/session-1/clone'
        # Без JSON тела API отвечает 415
        assert kwargs['json'] == {}

    def test_rotor_session_tracks(self):
        client, post = _make_client({'batchId': 'batch-2', 'unknownSession': False})
        feedback = SessionFeedback(SessionEvent('skip', '2024-01-01T12:00:00.000Z', '12345', 3), 'batch-1')

        result = client.rotor_session_tracks('session-1', ['12345:678'], [feedback])

        assert isinstance(result, RotorSessionTracks)
        args, kwargs = post.call_args
        assert args[0] == f'{BASE}/session/session-1/tracks'
        assert kwargs['json'] == {
            'queue': ['12345:678'],
            'feedbacks': [
                {
                    'event': {
                        'type': 'skip',
                        'timestamp': '2024-01-01T12:00:00.000Z',
                        'trackId': '12345',
                        'totalPlayedSeconds': 3,
                        'playable': None,
                    },
                    'batchId': 'batch-1',
                    'from': None,
                }
            ],
        }

    def test_rotor_session_tracks_without_queue(self):
        client, post = _make_client({})

        client.rotor_session_tracks('session-1')

        _, kwargs = post.call_args
        assert kwargs['json'] == {'queue': []}

    def test_rotor_session_feedback(self):
        client, post = _make_client({})
        event = SessionEvent(
            'playableItemStarted', '2024-01-01T12:00:00.000Z', playable=SessionPlayable('clip', id='1')
        )

        assert client.rotor_session_feedback('session-1', event, 'batch-1', 'radio-web') is True
        args, kwargs = post.call_args
        assert args[0] == f'{BASE}/session/session-1/feedback'
        assert kwargs['json'] == {
            'event': {
                'type': 'playableItemStarted',
                'timestamp': '2024-01-01T12:00:00.000Z',
                'trackId': None,
                'totalPlayedSeconds': None,
                'playable': {'type': 'clip', 'trackId': None, 'id': '1'},
            },
            'batchId': 'batch-1',
            'from': 'radio-web',
        }

    def test_rotor_session_feedback_radio_started(self):
        client, post = _make_client({})

        assert client.rotor_session_feedback_radio_started('session-1', 'batch-1', 'radio-web') is True
        _, kwargs = post.call_args
        assert kwargs['json']['event']['type'] == 'radioStarted'
        assert re.fullmatch(ISO_UTC, kwargs['json']['event']['timestamp'])
        assert kwargs['json']['batchId'] == 'batch-1'
        assert kwargs['json']['from'] == 'radio-web'

    def test_rotor_session_feedback_track_started(self):
        client, post = _make_client({})

        client.rotor_session_feedback_track_started('session-1', 12345, 'batch-1')

        _, kwargs = post.call_args
        assert kwargs['json']['event']['type'] == 'trackStarted'
        assert kwargs['json']['event']['trackId'] == '12345'
        assert kwargs['json']['batchId'] == 'batch-1'

    def test_rotor_session_feedback_track_finished(self):
        client, post = _make_client({})

        client.rotor_session_feedback_track_finished('session-1', '12345', 180.5, timestamp='2024-01-01T12:00:00.000Z')

        _, kwargs = post.call_args
        assert kwargs['json']['event'] == {
            'type': 'trackFinished',
            'timestamp': '2024-01-01T12:00:00.000Z',
            'trackId': '12345',
            'totalPlayedSeconds': 180.5,
            'playable': None,
        }

    def test_rotor_session_feedback_skip(self):
        client, post = _make_client({})

        client.rotor_session_feedback_skip('session-1', '12345', 7)

        _, kwargs = post.call_args
        assert kwargs['json']['event']['type'] == 'skip'
        assert kwargs['json']['event']['totalPlayedSeconds'] == 7

    def test_rotor_session_feedbacks(self):
        client, post = _make_client({})
        feedback = SessionFeedback(SessionEvent('radioStarted', '2024-01-01T12:00:00.000Z'))

        assert client.rotor_session_feedbacks('session-1', [feedback]) is True
        args, kwargs = post.call_args
        assert args[0] == f'{BASE}/session/session-1/feedbacks'
        assert kwargs['json'] == {'feedbacks': [feedback.to_dict(for_request=True)]}

    def test_rotor_sessions_feedbacks(self):
        client, post = _make_client({})
        feedback = SessionFeedback(SessionEvent('radioStarted', '2024-01-01T12:00:00.000Z'))
        sessions = [SessionFeedbacks('session-1', [feedback])]

        assert client.rotor_sessions_feedbacks(sessions) is True
        args, kwargs = post.call_args
        assert args[0] == f'{BASE}/sessions/feedbacks'
        assert kwargs['json'] == {
            'sessions': [{'sessionId': 'session-1', 'feedbacks': [feedback.to_dict(for_request=True)]}]
        }

    def test_rotor_combined_session_new(self):
        client, post = _make_client({'sessionId': 'combined-1', 'list': []})

        result = client.rotor_combined_session_new(
            ['CLIP', 'TRACK'], [CombinedSessionQueueItem('CLIP', '1')], child=False, allow_explicit=True
        )

        assert isinstance(result, CombinedSession)
        assert result.session_id == 'combined-1'
        args, kwargs = post.call_args
        assert args[0] == f'{BASE}/combined/session/new'
        assert kwargs['json'] == {
            'supportedTypes': ['CLIP', 'TRACK'],
            'queue': [{'type': 'CLIP', 'id': '1'}],
            'child': False,
            'allowExplicit': True,
        }

    def test_rotor_combined_session_next(self):
        client, post = _make_client({'batchId': 'batch-3', 'list': []})

        result = client.rotor_combined_session_next('combined-1')

        assert isinstance(result, CombinedSession)
        args, kwargs = post.call_args
        assert args[0] == f'{BASE}/combined/session/combined-1/next'
        # Без JSON тела API отвечает 415
        assert kwargs['json'] == {'queue': []}

    def test_rotor_combined_session_landing(self):
        client, post = _make_client({'title': 'Время клипов', 'list': []})

        result = client.rotor_combined_session_landing(['CLIP'])

        assert isinstance(result, CombinedSessionLanding)
        args, kwargs = post.call_args
        assert args[0] == f'{BASE}/combined/session/landing'
        assert kwargs['json'] == {'supportedTypes': ['CLIP']}
