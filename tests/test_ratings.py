from typing import Dict

from yandex_music import Client, JSONType, Ratings


class TestRatings:
    week = 4949
    month = 6597
    day = 5512

    def test_expected_values(self, ratings: Ratings) -> None:
        assert ratings.week == self.week
        assert ratings.month == self.month
        assert ratings.day == self.day

    def test_de_json_none(self, client: Client) -> None:
        assert Ratings.de_json({}, client) is None

    def test_de_json_required(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {'week': self.week, 'month': self.month}
        ratings = Ratings.de_json(json_dict, client)
        assert ratings is not None

        assert ratings.week == self.week
        assert ratings.month == self.month

    def test_de_json_all(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {'week': self.week, 'month': self.month, 'day': self.day}
        ratings = Ratings.de_json(json_dict, client)
        assert ratings is not None

        assert ratings.week == self.week
        assert ratings.month == self.month
        assert ratings.day == self.day

    def test_equality(self) -> None:
        a = Ratings(self.week, self.month)
        b = Ratings(10, self.month)
        c = Ratings(self.week, self.month, self.day)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
