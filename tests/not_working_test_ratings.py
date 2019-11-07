from yandex_music import Ratings


class TestRatings:
    week = None
    month = None
    day = None

    def test_expected_values(self, ratings):
        assert ratings.week == self.week
        assert ratings.month == self.month
        assert ratings.day == self.day

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
        pass
