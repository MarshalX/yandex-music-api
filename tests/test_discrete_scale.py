from typing import Dict

from yandex_music import Client, DiscreteScale, JSONType, Value


class TestDiscreteScale:
    type = 'discrete-scale'
    name = 'Настроение'

    def test_expected_values(self, discrete_scale: DiscreteScale, value: Value) -> None:
        assert discrete_scale.type == self.type
        assert discrete_scale.name == self.name
        assert discrete_scale.min == value
        assert discrete_scale.max == value

    def test_de_json_none(self, client: Client) -> None:
        assert DiscreteScale.de_json({}, client) is None

    def test_de_json_required(self, client: Client, value: Value) -> None:
        json_dict: Dict[str, JSONType] = {
            'type': self.type,
            'name': self.name,
            'min': value.to_dict(),
            'max': value.to_dict(),
        }
        discrete_scale = DiscreteScale.de_json(json_dict, client)
        assert discrete_scale is not None

        assert discrete_scale.type == self.type
        assert discrete_scale.name == self.name
        assert discrete_scale.min == value
        assert discrete_scale.max == value

    def test_de_json_all(self, client: Client, value: Value) -> None:
        json_dict: Dict[str, JSONType] = {
            'type': self.type,
            'name': self.name,
            'min': value.to_dict(),
            'max': value.to_dict(),
        }
        discrete_scale = DiscreteScale.de_json(json_dict, client)
        assert discrete_scale is not None

        assert discrete_scale.type == self.type
        assert discrete_scale.name == self.name
        assert discrete_scale.min == value
        assert discrete_scale.max == value

    def test_equality(self, value: Value) -> None:
        a = DiscreteScale(self.type, self.name, value, value)
        b = DiscreteScale('', self.name, value, value)
        c = DiscreteScale('', '', value, value)
        d = DiscreteScale(self.type, self.name, value, value)

        assert a != b != c
        assert hash(a) != hash(b) != hash(c)
        assert a is not b is not c

        assert a == d
