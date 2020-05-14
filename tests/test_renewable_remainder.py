from yandex_music import RenewableRemainder


class TestRenewableRemainder:
    days = 0

    def test_expected_values(self, renewable_remainder):
        assert renewable_remainder.days == self.days

    def test_de_json_none(self, client):
        assert RenewableRemainder.de_json({}, client) is None

    def test_de_json_required(self, client):
        json_dict = {'days': self.days}
        renewable_remainder = RenewableRemainder.de_json(json_dict, client)

        assert renewable_remainder.days == self.days

    def test_de_json_all(self, client):
        json_dict = {'days': self.days}
        renewable_remainder = RenewableRemainder.de_json(json_dict, client)

        assert renewable_remainder.days == self.days

    def test_equality(self):
        a = RenewableRemainder(self.days)
        b = RenewableRemainder(10)
        c = RenewableRemainder(self.days)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
