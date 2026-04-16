from yandex_music import ConcertFeedItem


class TestConcertFeedItem:
    type = 'concert_item'

    def test_expected_value(self, concert_feed_item, concert_feed_item_data):
        assert concert_feed_item.type == self.type
        assert concert_feed_item.data == concert_feed_item_data

    def test_de_json_none(self, client):
        assert ConcertFeedItem.de_json({}, client) is None

    def test_de_json_all(self, client, concert_feed_item_data):
        json_dict = {
            'type': self.type,
            'data': concert_feed_item_data.to_dict(),
        }
        concert_feed_item = ConcertFeedItem.de_json(json_dict, client)

        assert concert_feed_item.type == self.type
        assert concert_feed_item.data == concert_feed_item_data

    def test_equality(self, concert_feed_item_data):
        a = ConcertFeedItem(type=self.type, data=concert_feed_item_data)
        b = ConcertFeedItem(type='other_item', data=concert_feed_item_data)
        c = ConcertFeedItem(type=self.type, data=concert_feed_item_data)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
