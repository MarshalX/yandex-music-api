from yandex_music import ConcertTabConfig


class TestConcertTabConfig:
    def test_expected_value(self, concert_tab_config, concert_tab_config_data):
        assert concert_tab_config.config == concert_tab_config_data

    def test_de_json_none(self, client):
        assert ConcertTabConfig.de_json({}, client) is None

    def test_de_json_all(self, client, concert_tab_config_data):
        json_dict = {
            'config': concert_tab_config_data.to_dict(),
        }
        concert_tab_config = ConcertTabConfig.de_json(json_dict, client)

        assert concert_tab_config.config == concert_tab_config_data

    def test_equality(self, concert_tab_config_data):
        a = ConcertTabConfig(config=concert_tab_config_data)
        b = ConcertTabConfig(config=None)
        c = ConcertTabConfig(config=concert_tab_config_data)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
