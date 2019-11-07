from yandex_music import Normalization


class TestNormalization:
    gain = None
    peak = None

    def test_expected_values(self, normalization):
        assert normalization.gain == self.gain
        assert normalization.peak == self.peak

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
        pass
