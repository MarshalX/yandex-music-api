from typing import Dict

from yandex_music import Client, Enum, JSONType, Value


class TestEnum:
    type = 'enum'
    name = 'Язык'

    def test_expected_values(self, enum: Enum, value: Value) -> None:
        assert enum.type == self.type
        assert enum.name == self.name
        assert enum.possible_values == [value]

    def test_de_json_none(self, client: Client) -> None:
        assert Enum.de_json({}, client) is None

    def test_de_json_required(self, client: Client, value: Value) -> None:
        json_dict: Dict[str, JSONType] = {'type': self.type, 'name': self.name, 'possible_values': [value.to_dict()]}
        enum = Enum.de_json(json_dict, client)
        assert enum is not None

        assert enum.type == self.type
        assert enum.name == self.name
        assert enum.possible_values == [value]

    def test_de_json_all(self, client: Client, value: Value) -> None:
        json_dict: Dict[str, JSONType] = {'type': self.type, 'name': self.name, 'possible_values': [value.to_dict()]}
        enum = Enum.de_json(json_dict, client)
        assert enum is not None

        assert enum.type == self.type
        assert enum.name == self.name
        assert enum.possible_values == [value]

    def test_equality(self, value: Value) -> None:
        a = Enum(self.type, self.name, [value])
        b = Enum(self.type, '', [value])
        c = Enum(self.type, self.name, [value])

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
