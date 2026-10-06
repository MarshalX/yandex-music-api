from typing import Dict

from yandex_music import Client, Concert, ConcertDescription, ConcertInfo, ConcertMinPrice, Cover, JSONType


class TestConcertInfo:
    lead_artist_id = 100500

    def test_expected_value(
        self,
        concert_info: ConcertInfo,
        concert: Concert,
        concert_min_price: ConcertMinPrice,
        cover: Cover,
        concert_description: ConcertDescription,
    ) -> None:
        assert concert_info.concert == concert
        assert concert_info.min_price == concert_min_price
        assert concert_info.covers == [cover]
        assert concert_info.description == concert_description
        assert concert_info.lead_artist_id == self.lead_artist_id

    def test_de_json_none(self, client: Client) -> None:
        assert ConcertInfo.de_json({}, client) is None

    def test_de_json_all(
        self,
        client: Client,
        concert: Concert,
        concert_min_price: ConcertMinPrice,
        cover: Cover,
        concert_description: ConcertDescription,
    ) -> None:
        json_dict: Dict[str, JSONType] = {
            'concert': concert.to_dict(),
            'min_price': concert_min_price.to_dict(),
            'covers': [cover.to_dict()],
            'description': concert_description.to_dict(),
            'lead_artist_id': self.lead_artist_id,
        }
        concert_info = ConcertInfo.de_json(json_dict, client)
        assert concert_info is not None

        assert concert_info.concert == concert
        assert concert_info.min_price == concert_min_price
        assert concert_info.covers == [cover]
        assert concert_info.description == concert_description
        assert concert_info.lead_artist_id == self.lead_artist_id

    def test_equality(self, concert: Concert) -> None:
        a = ConcertInfo(concert=concert, lead_artist_id=self.lead_artist_id)
        b = ConcertInfo(concert=None, lead_artist_id=self.lead_artist_id)
        c = ConcertInfo(concert=concert, lead_artist_id=self.lead_artist_id)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
