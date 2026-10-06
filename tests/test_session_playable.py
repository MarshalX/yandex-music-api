from typing import Dict, Optional

from yandex_music import Client, JSONType, SessionPlayable


class TestSessionPlayable:
    type = 'track'
    track_id = '12345'
    id: Optional[str] = None

    def test_expected_values(self, session_playable: SessionPlayable) -> None:
        assert session_playable.type == self.type
        assert session_playable.track_id == self.track_id
        assert session_playable.id == self.id

    def test_de_json_none(self, client: Client) -> None:
        assert SessionPlayable.de_json({}, client) is None

    def test_de_json_all(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {'type': 'clip', 'id': '100500'}
        session_playable = SessionPlayable.de_json(json_dict, client)
        assert session_playable is not None

        assert session_playable.type == 'clip'
        assert session_playable.id == '100500'
        assert session_playable.track_id is None

    def test_to_dict_for_request(self, session_playable: SessionPlayable) -> None:
        assert session_playable.to_dict(for_request=True) == {'type': self.type, 'trackId': self.track_id, 'id': None}

    def test_equality(self) -> None:
        a = SessionPlayable(self.type, self.track_id)
        b = SessionPlayable(self.type, '54321')
        c = SessionPlayable(self.type, self.track_id)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
