from typing import Dict

from yandex_music import Client, ConcertFeed, ConcertFeedItem, JSONType


class TestConcertFeed:
    def test_expected_value(self, concert_feed: ConcertFeed, concert_feed_item: ConcertFeedItem) -> None:
        assert concert_feed.items == [concert_feed_item]

    def test_de_json_none(self, client: Client) -> None:
        assert ConcertFeed.de_json({}, client) is None

    def test_de_json_all(self, client: Client, concert_feed_item: ConcertFeedItem) -> None:
        json_dict: Dict[str, JSONType] = {
            'items': [concert_feed_item.to_dict()],
        }
        concert_feed = ConcertFeed.de_json(json_dict, client)
        assert concert_feed is not None

        assert concert_feed.items == [concert_feed_item]

    def test_equality(self, concert_feed_item: ConcertFeedItem) -> None:
        a = ConcertFeed(items=[concert_feed_item])
        b = ConcertFeed(items=[])
        c = ConcertFeed(items=[concert_feed_item])

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
