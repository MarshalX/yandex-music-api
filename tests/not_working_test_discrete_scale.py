import pytest

from yandex_music import DiscreteScale


@pytest.fixture(scope='class')
def discrete_scale(min, max):
    return DiscreteScale(TestDiscreteScale.type, TestDiscreteScale.name, min, max)


class TestDiscreteScale:
    type = None
    name = None

    def test_expected_values(self, discrete_scale, min, max):
        assert discrete_scale.type == self.type
        assert discrete_scale.name == self.name
        assert discrete_scale.min == min
        assert discrete_scale.max == max

    def test_de_json_required(self, client, min, max):
        json_dict = {'type': self.type, 'name': self.name, 'min': min, 'max': max}
        discrete_scale = DiscreteScale.de_json(json_dict, client)

        assert discrete_scale.type == self.type
        assert discrete_scale.name == self.name
        assert discrete_scale.min == min
        assert discrete_scale.max == max

    def test_de_json_all(self, client, min, max):
        json_dict = {'type': self.type, 'name': self.name, 'min': min, 'max': max}
        discrete_scale = DiscreteScale.de_json(json_dict, client)

        assert discrete_scale.type == self.type
        assert discrete_scale.name == self.name
        assert discrete_scale.min == min
        assert discrete_scale.max == max

    def test_equality(self):
        pass
