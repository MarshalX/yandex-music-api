from yandex_music import ConcertFeedItemData


class TestConcertFeedItemData:
    def test_expected_value(self, concert_feed_item_data, concert, concert_min_price):
        assert concert_feed_item_data.concert == concert
        assert concert_feed_item_data.min_price == concert_min_price

    def test_de_json_none(self, client):
        assert ConcertFeedItemData.de_json({}, client) is None

    def test_de_json_all(self, client, concert, concert_min_price):
        json_dict = {
            'concert': concert.to_dict(),
            'min_price': concert_min_price.to_dict(),
        }
        concert_feed_item_data = ConcertFeedItemData.de_json(json_dict, client)

        assert concert_feed_item_data.concert == concert
        assert concert_feed_item_data.min_price == concert_min_price

    def test_equality(self, concert, concert_min_price):
        a = ConcertFeedItemData(concert=concert, min_price=concert_min_price)
        b = ConcertFeedItemData(concert=None, min_price=concert_min_price)
        c = ConcertFeedItemData(concert=concert, min_price=concert_min_price)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
