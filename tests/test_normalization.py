from yandex_music import Normalization


class TestNormalization:
    gain = -3.89
    peak = 29168

    def test_expected_values(self, normalization):
        assert normalization.gain == self.gain
        assert normalization.peak == self.peak

    def test_de_json_none(self, client):
        assert Normalization.de_json({}, client) is None

    def test_de_json_required(self, client):
        json_dict = {'gain': self.gain, 'peak': self.peak}
        normalization = Normalization.de_json(json_dict, client)

        assert normalization.gain == self.gain
        assert normalization.peak == self.peak

    def test_de_json_all(self, client):
        json_dict = {'gain': self.gain, 'peak': self.peak}
        normalization = Normalization.de_json(json_dict, client)

        assert normalization.gain == self.gain
        assert normalization.peak == self.peak

    def test_equality(self):
        a = Normalization(self.gain, self.peak)
        b = Normalization(10, self.peak)
        c = Normalization(self.gain, 10)
        d = Normalization(10, 10)
        e = Normalization(self.gain, self.peak)

        assert a != b != c != d
        assert hash(a) != hash(b) != hash(c) != hash(d)
        assert a is not b is not c is not d

        assert a == e
