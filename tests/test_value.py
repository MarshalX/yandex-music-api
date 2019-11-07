import pytest

from yandex_music import Value


@pytest.fixture(scope='class')
def value():
    return Value(TestValue.value, TestValue.name)


class TestValue:
    value = 'not-russian'
    name = 'Иностранный'

    def test_expected_values(self, value):
        assert value.value == self.value
        assert value.name == self.name

    def test_de_json_required(self, client):
        json_dict = {'value': self.value, 'name': self.name}
        value = Value.de_json(json_dict, client)

        assert value.value == self.value
        assert value.name == self.name

    def test_de_json_all(self, client):
        json_dict = {'value': self.value, 'name': self.name}
        value = Value.de_json(json_dict, client)

        assert value.value == self.value
        assert value.name == self.name

    def test_equality(self):
        a = Value(self.value, self.name)
        b = Value(self.value, '')
        c = Value(self.value, self.name)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
