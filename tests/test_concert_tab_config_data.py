from yandex_music import ConcertTabConfigData, ConcertTabRange


class TestConcertTabConfigData:
    def test_expected_value(self, concert_tab_config_data, concert_tab_range):
        assert concert_tab_config_data.top == concert_tab_range
        assert concert_tab_config_data.feed == concert_tab_range

    def test_de_json_none(self, client):
        assert ConcertTabConfigData.de_json({}, client) is None

    def test_de_json_all(self, client, concert_tab_range):
        json_dict = {
            'top': concert_tab_range.to_dict(),
            'feed': concert_tab_range.to_dict(),
        }
        concert_tab_config_data = ConcertTabConfigData.de_json(json_dict, client)

        assert concert_tab_config_data.top == concert_tab_range
        assert concert_tab_config_data.feed == concert_tab_range

    def test_equality(self, concert_tab_range):
        other_range = ConcertTabRange(offset=5, limit=-1)
        a = ConcertTabConfigData(top=concert_tab_range, feed=concert_tab_range)
        b = ConcertTabConfigData(top=other_range, feed=concert_tab_range)
        c = ConcertTabConfigData(top=concert_tab_range, feed=concert_tab_range)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
