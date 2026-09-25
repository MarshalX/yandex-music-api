from yandex_music import SessionPlayable


class TestSessionPlayable:
    type = 'track'
    track_id = '12345'
    id = None

    def test_expected_values(self, session_playable):
        assert session_playable.type == self.type
        assert session_playable.track_id == self.track_id
        assert session_playable.id == self.id

    def test_de_json_none(self, client):
        assert SessionPlayable.de_json({}, client) is None

    def test_de_json_all(self, client):
        json_dict = {'type': 'clip', 'id': '100500'}
        session_playable = SessionPlayable.de_json(json_dict, client)

        assert session_playable.type == 'clip'
        assert session_playable.id == '100500'
        assert session_playable.track_id is None

    def test_to_dict_for_request(self, session_playable):
        assert session_playable.to_dict(for_request=True) == {'type': self.type, 'trackId': self.track_id, 'id': None}

    def test_equality(self):
        a = SessionPlayable(self.type, self.track_id)
        b = SessionPlayable(self.type, '54321')
        c = SessionPlayable(self.type, self.track_id)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
