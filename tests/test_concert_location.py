from yandex_music import ConcertLocation


class TestConcertLocation:
    id = 213
    name = 'Москва'

    def test_expected_value(self, concert_location):
        assert concert_location.id == self.id
        assert concert_location.name == self.name

    def test_de_json_none(self, client):
        assert ConcertLocation.de_json({}, client) is None

    def test_de_json_all(self, client):
        json_dict = {
            'id': self.id,
            'name': self.name,
        }
        concert_location = ConcertLocation.de_json(json_dict, client)

        assert concert_location.id == self.id
        assert concert_location.name == self.name

    def test_equality(self):
        a = ConcertLocation(id=self.id, name=self.name)
        b = ConcertLocation(id=2, name='Санкт-Петербург')
        c = ConcertLocation(id=self.id, name=self.name)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
