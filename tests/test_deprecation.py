from typing import Dict

from yandex_music import Client, Deprecation, JSONType


class TestDeprecation:
    target_album_id = 11084011
    status = 'duplicate-of'
    done = True

    def test_expected_values(self, deprecation: Deprecation) -> None:
        assert deprecation.target_album_id == self.target_album_id
        assert deprecation.status == self.status
        assert deprecation.done == self.done

    def test_de_json_none(self, client: Client) -> None:
        assert Deprecation.de_json({}, client) is None

    def test_de_json_required(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {
            'target_album_id': self.target_album_id,
            'status': self.status,
            'done': self.done,
        }
        deprecation = Deprecation.de_json(json_dict, client)
        assert deprecation is not None

        assert deprecation.target_album_id == self.target_album_id
        assert deprecation.status == self.status
        assert deprecation.done == self.done

    def test_de_json_all(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {
            'target_album_id': self.target_album_id,
            'status': self.status,
            'done': self.done,
        }
        deprecation = Deprecation.de_json(json_dict, client)
        assert deprecation is not None

        assert deprecation.target_album_id == self.target_album_id
        assert deprecation.status == self.status
        assert deprecation.done == self.done

    def test_equality(self) -> None:
        a = Deprecation(self.target_album_id, self.status, self.done)
        b = Deprecation(self.target_album_id, self.status, False)
        c = Deprecation(self.target_album_id, self.status, self.done)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
