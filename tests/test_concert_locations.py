from yandex_music import ConcertLocations


class TestConcertLocations:
    def test_expected_value(self, concert_locations, concert_location):
        assert concert_locations.locations == [concert_location]

    def test_de_json_none(self, client):
        assert ConcertLocations.de_json({}, client) is None

    def test_de_json_all(self, client, concert_location):
        json_dict = {
            'locations': [concert_location.to_dict()],
        }
        concert_locations = ConcertLocations.de_json(json_dict, client)

        assert concert_locations.locations == [concert_location]

    def test_equality(self, concert_location):
        other_location = type(concert_location)(id=2, name='Санкт-Петербург')
        a = ConcertLocations(locations=[concert_location])
        b = ConcertLocations(locations=[other_location])
        c = ConcertLocations(locations=[concert_location])

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
