from yandex_music import ConcertTabRange


class TestConcertTabRange:
    offset = 0
    limit = 5

    def test_expected_value(self, concert_tab_range):
        assert concert_tab_range.offset == self.offset
        assert concert_tab_range.limit == self.limit

    def test_de_json_none(self, client):
        assert ConcertTabRange.de_json({}, client) is None

    def test_de_json_all(self, client):
        json_dict = {
            'offset': self.offset,
            'limit': self.limit,
        }
        concert_tab_range = ConcertTabRange.de_json(json_dict, client)

        assert concert_tab_range.offset == self.offset
        assert concert_tab_range.limit == self.limit

    def test_equality(self):
        a = ConcertTabRange(offset=self.offset, limit=self.limit)
        b = ConcertTabRange(offset=5, limit=-1)
        c = ConcertTabRange(offset=self.offset, limit=self.limit)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
