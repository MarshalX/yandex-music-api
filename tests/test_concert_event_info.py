from typing import Dict

from yandex_music import Client, ConcertEventInfo, JSONType


class TestConcertEventInfo:
    type = 'concert'

    def test_expected_value(self, concert_event_info: ConcertEventInfo) -> None:
        assert concert_event_info.type == self.type

    def test_de_json_none(self, client: Client) -> None:
        assert ConcertEventInfo.de_json({}, client) is None

    def test_de_json_all(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {
            'type': self.type,
        }
        concert_event_info = ConcertEventInfo.de_json(json_dict, client)
        assert concert_event_info is not None

        assert concert_event_info.type == self.type

    def test_equality(self) -> None:
        a = ConcertEventInfo(type=self.type)
        b = ConcertEventInfo(type='festival')
        c = ConcertEventInfo(type=self.type)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
