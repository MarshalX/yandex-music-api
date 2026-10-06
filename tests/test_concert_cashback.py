from typing import Dict

from yandex_music import Client, ConcertCashback, JSONType


class TestConcertCashback:
    title = 'Кешбэк до 20%'
    value_percent = 20

    def test_expected_value(self, concert_cashback: ConcertCashback) -> None:
        assert concert_cashback.title == self.title
        assert concert_cashback.value_percent == self.value_percent

    def test_de_json_none(self, client: Client) -> None:
        assert ConcertCashback.de_json({}, client) is None

    def test_de_json_all(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {
            'title': self.title,
            'value_percent': self.value_percent,
        }
        concert_cashback = ConcertCashback.de_json(json_dict, client)
        assert concert_cashback is not None

        assert concert_cashback.title == self.title
        assert concert_cashback.value_percent == self.value_percent

    def test_equality(self) -> None:
        a = ConcertCashback(title=self.title, value_percent=self.value_percent)
        b = ConcertCashback(title='Кешбэк до 10%', value_percent=10)
        c = ConcertCashback(title=self.title, value_percent=self.value_percent)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
