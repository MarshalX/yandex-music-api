from typing import Dict

from yandex_music import Client, JSONType, Normalization


class TestNormalization:
    gain = -3.89
    peak = 29168

    def test_expected_values(self, normalization: Normalization) -> None:
        assert normalization.gain == self.gain
        assert normalization.peak == self.peak

    def test_de_json_none(self, client: Client) -> None:
        assert Normalization.de_json({}, client) is None

    def test_de_json_required(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {'gain': self.gain, 'peak': self.peak}
        normalization = Normalization.de_json(json_dict, client)
        assert normalization is not None

        assert normalization.gain == self.gain
        assert normalization.peak == self.peak

    def test_de_json_all(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {'gain': self.gain, 'peak': self.peak}
        normalization = Normalization.de_json(json_dict, client)
        assert normalization is not None

        assert normalization.gain == self.gain
        assert normalization.peak == self.peak

    def test_equality(self) -> None:
        a = Normalization(self.gain, self.peak)
        b = Normalization(10, self.peak)
        c = Normalization(self.gain, 10)
        d = Normalization(10, 10)
        e = Normalization(self.gain, self.peak)

        assert a != b != c != d
        assert hash(a) != hash(b) != hash(c) != hash(d)
        assert a is not b is not c is not d

        assert a == e
