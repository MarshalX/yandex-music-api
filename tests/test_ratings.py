from yandex_music import Ratings


class TestRatings:
    week = 4949
    month = 6597
    day = 5512

    def test_expected_values(self, ratings):
        assert ratings.week == self.week
        assert ratings.month == self.month
        assert ratings.day == self.day

    def test_de_json_none(self, client):
        assert Ratings.de_json({}, client) is None

    def test_de_json_required(self, client):
        json_dict = {'week': self.week, 'month': self.month}
        ratings = Ratings.de_json(json_dict, client)

        assert ratings.week == self.week
        assert ratings.month == self.month

    def test_de_json_all(self, client):
        json_dict = {'week': self.week, 'month': self.month, 'day': self.day}
        ratings = Ratings.de_json(json_dict, client)

        assert ratings.week == self.week
        assert ratings.month == self.month
        assert ratings.day == self.day

    def test_equality(self):
        a = Ratings(self.week, self.month)
        b = Ratings(10, self.month)
        c = Ratings(self.week, self.month, self.day)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
