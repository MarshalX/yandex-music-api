from yandex_music import NonAutoRenewable


class TestNonAutoRenewable:
    start = '2019-05-27T20:34:21+03:00'
    end = '2020-09-01T20:34:21+03:00'

    def test_expected_values(self, non_auto_renewable):
        assert non_auto_renewable.start == self.start
        assert non_auto_renewable.end == self.end

    def test_de_json_none(self, client):
        assert NonAutoRenewable.de_json({}, client) is None

    def test_de_json_required(self, client):
        json_dict = {'start': self.start, 'end': self.end}
        non_auto_renewable = NonAutoRenewable.de_json(json_dict, client)

        assert non_auto_renewable.start == self.start
        assert non_auto_renewable.end == self.end

    def test_de_json_all(self, client):
        json_dict = {'start': self.start, 'end': self.end}
        non_auto_renewable = NonAutoRenewable.de_json(json_dict, client)

        assert non_auto_renewable.start == self.start
        assert non_auto_renewable.end == self.end

    def test_equality(self):
        a = NonAutoRenewable(self.start, self.end)
        b = NonAutoRenewable('', self.end)
        c = NonAutoRenewable(self.start, self.end)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
