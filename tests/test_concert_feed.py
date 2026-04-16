from yandex_music import ConcertFeed


class TestConcertFeed:
    def test_expected_value(self, concert_feed, concert_feed_item):
        assert concert_feed.items == [concert_feed_item]

    def test_de_json_none(self, client):
        assert ConcertFeed.de_json({}, client) is None

    def test_de_json_all(self, client, concert_feed_item):
        json_dict = {
            'items': [concert_feed_item.to_dict()],
        }
        concert_feed = ConcertFeed.de_json(json_dict, client)

        assert concert_feed.items == [concert_feed_item]

    def test_equality(self, concert_feed_item):
        a = ConcertFeed(items=[concert_feed_item])
        b = ConcertFeed(items=[])
        c = ConcertFeed(items=[concert_feed_item])

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
