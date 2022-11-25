import pytest

from yandex_music import r128


class TestR128:
    i = -13.12
    tp = 0.63

    def test_expected_values(self, r128_):
        assert r128_.i == self.i
        assert r128_.tp == self.tp

    def test_de_json_none(self, client):
        assert r128.de_json({}, client) is None

    def test_de_json_required(self, client):
        json_dict = {'i': self.i, 'tp': self.tp}
        _r128 = r128.de_json(json_dict, client)

        assert _r128.i == self.i
        assert _r128.tp == self.tp

    def test_equality(self):
        a = r128(self.i, self.tp)
        b = r128(-8.98, self.tp)
        c = r128(self.i, self.tp)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
