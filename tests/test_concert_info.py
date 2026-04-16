from yandex_music import ConcertInfo


class TestConcertInfo:
    lead_artist_id = 100500

    def test_expected_value(self, concert_info, concert, concert_min_price, cover, concert_description):
        assert concert_info.concert == concert
        assert concert_info.min_price == concert_min_price
        assert concert_info.covers == [cover]
        assert concert_info.description == concert_description
        assert concert_info.lead_artist_id == self.lead_artist_id

    def test_de_json_none(self, client):
        assert ConcertInfo.de_json({}, client) is None

    def test_de_json_all(self, client, concert, concert_min_price, cover, concert_description):
        json_dict = {
            'concert': concert.to_dict(),
            'min_price': concert_min_price.to_dict(),
            'covers': [cover.to_dict()],
            'description': concert_description.to_dict(),
            'lead_artist_id': self.lead_artist_id,
        }
        concert_info = ConcertInfo.de_json(json_dict, client)

        assert concert_info.concert == concert
        assert concert_info.min_price == concert_min_price
        assert concert_info.covers == [cover]
        assert concert_info.description == concert_description
        assert concert_info.lead_artist_id == self.lead_artist_id

    def test_equality(self, concert):
        a = ConcertInfo(concert=concert, lead_artist_id=self.lead_artist_id)
        b = ConcertInfo(concert=None, lead_artist_id=self.lead_artist_id)
        c = ConcertInfo(concert=concert, lead_artist_id=self.lead_artist_id)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
