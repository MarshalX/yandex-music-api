from yandex_music import Price


class TestPrice:
    amount = None
    currency = None

    def test_expected_values(self, price):
        assert price.amount == self.amount
        assert price.currency == self.currency

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
        pass
