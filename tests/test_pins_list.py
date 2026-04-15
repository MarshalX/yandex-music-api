from yandex_music import PinsList


class TestPinsList:
    def test_expected_value(self, pins_list, pin_artist):
        assert pins_list.pins == [pin_artist]

    def test_de_json_none(self, client):
        assert PinsList.de_json({}, client) is None

    def test_de_json_all(self, client, pin_artist):
        json_dict = {
            'pins': [pin_artist.to_dict()],
        }
        pins_list = PinsList.de_json(json_dict, client)

        assert pins_list.pins == [pin_artist]

    def test_equality(self, pin_artist):
        a = PinsList(pins=[pin_artist])
        b = PinsList(pins=None)
        c = PinsList(pins=[pin_artist])

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
