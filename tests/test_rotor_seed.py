from yandex_music import RotorSeed


class TestRotorSeed:
    type = 'genre'
    tag = 'rock'
    value = 'rock'

    def test_expected_values(self, rotor_seed):
        assert rotor_seed.type == self.type
        assert rotor_seed.tag == self.tag
        assert rotor_seed.value == self.value

    def test_de_json_none(self, client):
        assert RotorSeed.de_json({}, client) is None

    def test_de_list_none(self, client):
        assert RotorSeed.de_list([], client) == []

    def test_de_json_all(self, client):
        json_dict = {'type': self.type, 'tag': self.tag, 'value': self.value}
        rotor_seed = RotorSeed.de_json(json_dict, client)

        assert rotor_seed.type == self.type
        assert rotor_seed.tag == self.tag
        assert rotor_seed.value == self.value

    def test_equality(self):
        a = RotorSeed(self.type, self.tag, self.value)
        b = RotorSeed('user', 'onyourwave', 'onyourwave')
        c = RotorSeed(self.type, self.tag, self.value)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
