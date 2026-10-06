from typing import Dict

from yandex_music import Client, JSONType, Major


class TestMajor:
    id = 4
    name = 'WARNER'

    def test_expected_values(self, major: Major) -> None:
        assert major.id == self.id
        assert major.name == self.name

    def test_de_json_none(self, client: Client) -> None:
        assert Major.de_json({}, client) is None

    def test_de_json_required(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {'id': self.id, 'name': self.name}
        major = Major.de_json(json_dict, client)
        assert major is not None

        assert major.id == self.id
        assert major.name == self.name

    def test_de_json_all(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {'id': self.id, 'name': self.name}
        major = Major.de_json(json_dict, client)
        assert major is not None

        assert major.id == self.id
        assert major.name == self.name

    def test_equality(self) -> None:
        a = Major(self.id, self.name)
        b = Major(10, self.name)
        c = Major(self.id, self.name)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
