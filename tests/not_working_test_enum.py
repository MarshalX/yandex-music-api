import pytest

from yandex_music import Enum


@pytest.fixture(scope='class')
def enum(possible_values):
    return Enum(TestEnum.type, TestEnum.name, possible_values)


class TestEnum:
    type = None
    name = None

    def test_expected_values(self, enum, possible_values):
        assert enum.type == self.type
        assert enum.name == self.name
        assert enum.possible_values == possible_values

    def test_de_json_required(self, client, possible_values):
        json_dict = {'type': self.type, 'name': self.name, 'possible_values': possible_values}
        enum = Enum.de_json(json_dict, client)

        assert enum.type == self.type
        assert enum.name == self.name
        assert enum.possible_values == possible_values

    def test_de_json_all(self, client, possible_values):
        json_dict = {'type': self.type, 'name': self.name, 'possible_values': possible_values}
        enum = Enum.de_json(json_dict, client)

        assert enum.type == self.type
        assert enum.name == self.name
        assert enum.possible_values == possible_values

    def test_equality(self):
        pass
