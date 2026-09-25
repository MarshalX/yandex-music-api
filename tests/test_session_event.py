from yandex_music import SessionEvent


class TestSessionEvent:
    type = 'trackFinished'
    timestamp = '2024-01-01T12:00:00.000Z'
    track_id = '12345:67890'
    total_played_seconds = 42.5

    def test_expected_values(self, session_event, session_playable):
        assert session_event.type == self.type
        assert session_event.timestamp == self.timestamp
        assert session_event.track_id == self.track_id
        assert session_event.total_played_seconds == self.total_played_seconds
        assert session_event.playable == session_playable

    def test_de_json_none(self, client):
        assert SessionEvent.de_json({}, client) is None

    def test_de_json_all(self, client, session_playable):
        json_dict = {
            'type': self.type,
            'timestamp': self.timestamp,
            'trackId': self.track_id,
            'totalPlayedSeconds': self.total_played_seconds,
            'playable': session_playable.to_dict(),
        }
        session_event = SessionEvent.de_json(json_dict, client)

        assert session_event.type == self.type
        assert session_event.timestamp == self.timestamp
        assert session_event.track_id == self.track_id
        assert session_event.total_played_seconds == self.total_played_seconds
        assert session_event.playable == session_playable

    def test_to_dict_for_request(self, session_event, session_playable):
        assert session_event.to_dict(for_request=True) == {
            'type': self.type,
            'timestamp': self.timestamp,
            'trackId': self.track_id,
            'totalPlayedSeconds': self.total_played_seconds,
            'playable': session_playable.to_dict(for_request=True),
        }

    def test_equality(self):
        a = SessionEvent(self.type, self.timestamp, self.track_id)
        b = SessionEvent('skip', self.timestamp, self.track_id)
        c = SessionEvent(self.type, self.timestamp, self.track_id)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
