from yandex_music import DiscreteScale


class TestDiscreteScale:
    type = 'discrete-scale'
    name = 'Настроение'

    def test_expected_values(self, discrete_scale, value):
        assert discrete_scale.type == self.type
        assert discrete_scale.name == self.name
        assert discrete_scale.min == value
        assert discrete_scale.max == value

    def test_de_json_none(self, client):
        assert DiscreteScale.de_json({}, client) is None

    def test_de_json_required(self, client, value):
        json_dict = {'type': self.type, 'name': self.name, 'min': value.to_dict(), 'max': value.to_dict()}
        discrete_scale = DiscreteScale.de_json(json_dict, client)

        assert discrete_scale.type == self.type
        assert discrete_scale.name == self.name
        assert discrete_scale.min == value
        assert discrete_scale.max == value

    def test_de_json_all(self, client, value):
        json_dict = {'type': self.type, 'name': self.name, 'min': value.to_dict(), 'max': value.to_dict()}
        discrete_scale = DiscreteScale.de_json(json_dict, client)

        assert discrete_scale.type == self.type
        assert discrete_scale.name == self.name
        assert discrete_scale.min == value
        assert discrete_scale.max == value

    def test_equality(self, value):
        a = DiscreteScale(self.type, self.name, value, value)
        b = DiscreteScale('', self.name, value, value)
        c = DiscreteScale('', '', value, value)
        d = DiscreteScale(self.type, self.name, value, value)

        assert a != b != c
        assert hash(a) != hash(b) != hash(c)
        assert a is not b is not c

        assert a == d
