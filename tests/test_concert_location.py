from typing import Dict

from yandex_music import Client, ConcertLocation, JSONType


class TestConcertLocation:
    id = 213
    name = 'Москва'

    def test_expected_value(self, concert_location: ConcertLocation) -> None:
        assert concert_location.id == self.id
        assert concert_location.name == self.name

    def test_de_json_none(self, client: Client) -> None:
        assert ConcertLocation.de_json({}, client) is None

    def test_de_json_all(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {
            'id': self.id,
            'name': self.name,
        }
        concert_location = ConcertLocation.de_json(json_dict, client)
        assert concert_location is not None

        assert concert_location.id == self.id
        assert concert_location.name == self.name

    def test_equality(self) -> None:
        a = ConcertLocation(id=self.id, name=self.name)
        b = ConcertLocation(id=2, name='Санкт-Петербург')
        c = ConcertLocation(id=self.id, name=self.name)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
