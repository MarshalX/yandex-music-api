from yandex_music import WaveDefaultStation


class TestWaveDefaultStation:
    station_id = 'user:12345'
    title = 'Моя волна'
    rup_title = 'Моя волна'
    rup_description = 'Музыка для вас на каждый день'

    def test_expected_values(self, wave_default_station):
        assert wave_default_station.station_id == self.station_id
        assert wave_default_station.title == self.title
        assert wave_default_station.rup_title == self.rup_title
        assert wave_default_station.rup_description == self.rup_description

    def test_de_json_none(self, client):
        assert WaveDefaultStation.de_json({}, client) is None

    def test_de_json_all(self, client):
        json_dict = {
            'stationId': self.station_id,
            'title': self.title,
            'rupTitle': self.rup_title,
            'rupDescription': self.rup_description,
        }
        wave_default_station = WaveDefaultStation.de_json(json_dict, client)

        assert wave_default_station.station_id == self.station_id
        assert wave_default_station.title == self.title
        assert wave_default_station.rup_title == self.rup_title
        assert wave_default_station.rup_description == self.rup_description

    def test_equality(self):
        a = WaveDefaultStation(self.station_id, self.title)
        b = WaveDefaultStation('user:54321', self.title)
        c = WaveDefaultStation(self.station_id, self.title)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
