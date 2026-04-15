from yandex_music import TrackCredit


class TestTrackCredit:
    title = 'Автор музыки'
    value = 'Тестовый Исполнитель'

    def test_expected_value(self, track_credit):
        assert track_credit.title == self.title
        assert track_credit.value == self.value

    def test_de_json_none(self, client):
        assert TrackCredit.de_json({}, client) is None

    def test_de_json_all(self, client):
        json_dict = {
            'title': self.title,
            'value': self.value,
        }
        track_credit = TrackCredit.de_json(json_dict, client)

        assert track_credit.title == self.title
        assert track_credit.value == self.value

    def test_equality(self):
        a = TrackCredit(title=self.title, value=self.value)
        b = TrackCredit(title='Лейбл', value=self.value)
        c = TrackCredit(title=self.title, value=self.value)

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
