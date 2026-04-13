from yandex_music import ConcertEventInfo


class TestConcertEventInfo:
    type = 'concert'

    def test_expected_value(self, concert_event_info):
        assert concert_event_info.type == self.type

    def test_de_json_none(self, client):
        assert ConcertEventInfo.de_json({}, client) is None

    def test_de_json_all(self, client):
        json_dict = {
            'type': self.type,
        }
        concert_event_info = ConcertEventInfo.de_json(json_dict, client)

        assert concert_event_info.type == self.type

    def test_equality(self):
        a = ConcertEventInfo(type=self.type)
        b = ConcertEventInfo(type='festival')
        c = ConcertEventInfo(type=self.type)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
