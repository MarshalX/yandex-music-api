from typing import Dict

from yandex_music import Client, ConcertTabConfigData, ConcertTabRange, JSONType


class TestConcertTabConfigData:
    def test_expected_value(
        self, concert_tab_config_data: ConcertTabConfigData, concert_tab_range: ConcertTabRange
    ) -> None:
        assert concert_tab_config_data.top == concert_tab_range
        assert concert_tab_config_data.feed == concert_tab_range

    def test_de_json_none(self, client: Client) -> None:
        assert ConcertTabConfigData.de_json({}, client) is None

    def test_de_json_all(self, client: Client, concert_tab_range: ConcertTabRange) -> None:
        json_dict: Dict[str, JSONType] = {
            'top': concert_tab_range.to_dict(),
            'feed': concert_tab_range.to_dict(),
        }
        concert_tab_config_data = ConcertTabConfigData.de_json(json_dict, client)
        assert concert_tab_config_data is not None

        assert concert_tab_config_data.top == concert_tab_range
        assert concert_tab_config_data.feed == concert_tab_range

    def test_equality(self, concert_tab_range: ConcertTabRange) -> None:
        other_range = ConcertTabRange(offset=5, limit=-1)
        a = ConcertTabConfigData(top=concert_tab_range, feed=concert_tab_range)
        b = ConcertTabConfigData(top=other_range, feed=concert_tab_range)
        c = ConcertTabConfigData(top=concert_tab_range, feed=concert_tab_range)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
