from typing import Dict

from yandex_music import Client, ConcertTabConfig, ConcertTabConfigData, JSONType


class TestConcertTabConfig:
    def test_expected_value(
        self, concert_tab_config: ConcertTabConfig, concert_tab_config_data: ConcertTabConfigData
    ) -> None:
        assert concert_tab_config.config == concert_tab_config_data

    def test_de_json_none(self, client: Client) -> None:
        assert ConcertTabConfig.de_json({}, client) is None

    def test_de_json_all(self, client: Client, concert_tab_config_data: ConcertTabConfigData) -> None:
        json_dict: Dict[str, JSONType] = {
            'config': concert_tab_config_data.to_dict(),
        }
        concert_tab_config = ConcertTabConfig.de_json(json_dict, client)
        assert concert_tab_config is not None

        assert concert_tab_config.config == concert_tab_config_data

    def test_equality(self, concert_tab_config_data: ConcertTabConfigData) -> None:
        a = ConcertTabConfig(config=concert_tab_config_data)
        b = ConcertTabConfig(config=None)
        c = ConcertTabConfig(config=concert_tab_config_data)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
