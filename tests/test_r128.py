from yandex_music import R128


class TestR128:
    i = -13.12
    tp = 0.63
    important_secs = 303

    def test_expected_values(self, r_128):
        assert r_128.i == self.i
        assert r_128.tp == self.tp
        assert r_128.important_secs == self.important_secs

    def test_de_json_none(self, client):
        assert R128.de_json({}, client) is None

    def test_de_json_required(self, client):
        json_dict = {'i': self.i, 'tp': self.tp}
        r128 = R128.de_json(json_dict, client)

        assert r128.i == self.i
        assert r128.tp == self.tp

    def test_de_json_all(self, client):
        json_dict = {'i': self.i, 'tp': self.tp, 'importantSecs': self.important_secs}
        r128 = R128.de_json(json_dict, client)

        assert r128.i == self.i
        assert r128.tp == self.tp
        assert r128.important_secs == self.important_secs

    def test_equality(self):
        a = R128(self.i, self.tp)
        b = R128(-8.98, self.tp)
        c = R128(self.i, self.tp)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
