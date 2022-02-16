from yandex_music import Enum


class TestEnum:
    type = 'enum'
    name = 'Язык'

    def test_expected_values(self, enum, value):
        assert enum.type == self.type
        assert enum.name == self.name
        assert enum.possible_values == [value]

    def test_de_json_none(self, client):
        assert Enum.de_json({}, client) is None

    def test_de_json_required(self, client, value):
        json_dict = {'type': self.type, 'name': self.name, 'possible_values': [value.to_dict()]}
        enum = Enum.de_json(json_dict, client)

        assert enum.type == self.type
        assert enum.name == self.name
        assert enum.possible_values == [value]

    def test_de_json_all(self, client, value):
        json_dict = {'type': self.type, 'name': self.name, 'possible_values': [value.to_dict()]}
        enum = Enum.de_json(json_dict, client)

        assert enum.type == self.type
        assert enum.name == self.name
        assert enum.possible_values == [value]

    def test_equality(self, value):
        a = Enum(self.type, self.name, [value])
        b = Enum(self.type, '', [value])
        c = Enum(self.type, self.name, [value])

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
