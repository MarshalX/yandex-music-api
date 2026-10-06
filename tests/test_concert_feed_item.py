from typing import Dict

from yandex_music import Client, ConcertFeedItem, ConcertFeedItemData, JSONType


class TestConcertFeedItem:
    type = 'concert_item'

    def test_expected_value(
        self, concert_feed_item: ConcertFeedItem, concert_feed_item_data: ConcertFeedItemData
    ) -> None:
        assert concert_feed_item.type == self.type
        assert concert_feed_item.data == concert_feed_item_data

    def test_de_json_none(self, client: Client) -> None:
        assert ConcertFeedItem.de_json({}, client) is None

    def test_de_json_all(self, client: Client, concert_feed_item_data: ConcertFeedItemData) -> None:
        json_dict: Dict[str, JSONType] = {
            'type': self.type,
            'data': concert_feed_item_data.to_dict(),
        }
        concert_feed_item = ConcertFeedItem.de_json(json_dict, client)
        assert concert_feed_item is not None

        assert concert_feed_item.type == self.type
        assert concert_feed_item.data == concert_feed_item_data

    def test_equality(self, concert_feed_item_data: ConcertFeedItemData) -> None:
        a = ConcertFeedItem(type=self.type, data=concert_feed_item_data)
        b = ConcertFeedItem(type='other_item', data=concert_feed_item_data)
        c = ConcertFeedItem(type=self.type, data=concert_feed_item_data)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
