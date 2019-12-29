from yandex_music import Price


class TestPrice:
    amount = 99
    currency = 'RUB'

    def test_expected_values(self, price):
        assert price.amount == self.amount
        assert price.currency == self.currency

    def test_de_json_none(self, client):
        assert Price.de_json({}, client) is None

    def test_de_json_required(self, client):
        json_dict = {'amount': self.amount, 'currency': self.currency}
        price = Price.de_json(json_dict, client)

        assert price.amount == self.amount
        assert price.currency == self.currency

    def test_de_json_all(self, client):
        json_dict = {'amount': self.amount, 'currency': self.currency}
        price = Price.de_json(json_dict, client)

        assert price.amount == self.amount
        assert price.currency == self.currency

    def test_equality(self):
        a = Price(self.amount, self.currency)
        b = Price(10, self.currency)
        c = Price(self.amount, 'USD')
        d = Price(self.amount, self.currency)

        assert a != b != c
        assert hash(a) != hash(b) != hash(c)
        assert a is not b is not c

        assert a == d
