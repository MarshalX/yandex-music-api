from yandex_music import StationData


class TestStationData:
    name = 'Marshal\'s station'

    def test_expected_values(self, station_data):
        assert station_data.name == self.name

    def test_de_json_none(self, client):
        assert StationData.de_json({}, client) is None

    def test_de_json_required(self, client):
        json_dict = {'name': self.name}
        station_data = StationData.de_json(json_dict, client)

        assert station_data.name == self.name

    def test_de_json_all(self, client):
        json_dict = {'name': self.name}
        station_data = StationData.de_json(json_dict, client)

        assert station_data.name == self.name

    def test_equality(self):
        a = StationData(self.name)
        b = StationData('')
        c = StationData(self.name)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
