from typing import Dict

from yandex_music import Client, ConcertMinPrice, JSONType


class TestConcertMinPrice:
    value = 2500
    currency = 'RUB'
    currency_symbol = '₽'

    def test_expected_value(self, concert_min_price: ConcertMinPrice) -> None:
        assert concert_min_price.value == self.value
        assert concert_min_price.currency == self.currency
        assert concert_min_price.currency_symbol == self.currency_symbol

    def test_de_json_none(self, client: Client) -> None:
        assert ConcertMinPrice.de_json({}, client) is None

    def test_de_json_all(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {
            'value': self.value,
            'currency': self.currency,
            'currency_symbol': self.currency_symbol,
        }
        concert_min_price = ConcertMinPrice.de_json(json_dict, client)
        assert concert_min_price is not None

        assert concert_min_price.value == self.value
        assert concert_min_price.currency == self.currency
        assert concert_min_price.currency_symbol == self.currency_symbol

    def test_equality(self) -> None:
        a = ConcertMinPrice(value=self.value, currency=self.currency)
        b = ConcertMinPrice(value=1000, currency='USD')
        c = ConcertMinPrice(value=self.value, currency=self.currency)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
