from yandex_music import StationResult


class TestStationResult:
    explanation = ''
    prerolls = []

    def test_expected_values(self, station_result, station, rotor_settings, ad_params):
        assert station_result.station == station
        assert station_result.settings == rotor_settings
        assert station_result.settings2 == rotor_settings
        assert station_result.ad_params == ad_params
        assert station_result.explanation == self.explanation
        assert station_result.prerolls == self.prerolls

    def test_de_json_none(self, client):
        assert StationResult.de_json({}, client) is None

    def test_de_list_none(self, client):
        assert StationResult.de_list({}, client) == []

    def test_de_json_required(self, client, station, rotor_settings, ad_params):
        json_dict = {
            'station': station.to_dict(),
            'settings': rotor_settings.to_dict(),
            'settings2': rotor_settings.to_dict(),
            'ad_params': ad_params.to_dict(),
        }
        station_result = StationResult.de_json(json_dict, client)

        assert station_result.station == station
        assert station_result.settings == rotor_settings
        assert station_result.settings2 == rotor_settings
        assert station_result.ad_params == ad_params

    def test_de_json_all(self, client, station, rotor_settings, ad_params):
        json_dict = {
            'station': station.to_dict(),
            'settings': rotor_settings.to_dict(),
            'settings2': rotor_settings.to_dict(),
            'ad_params': ad_params.to_dict(),
            'explanation': self.explanation,
            'prerolls': self.prerolls,
        }
        station_result = StationResult.de_json(json_dict, client)

        assert station_result.station == station
        assert station_result.settings == rotor_settings
        assert station_result.settings2 == rotor_settings
        assert station_result.ad_params == ad_params
        assert station_result.explanation == self.explanation
        assert station_result.prerolls == self.prerolls

    def test_equality(self, station, rotor_settings, ad_params):
        a = StationResult(station, rotor_settings, rotor_settings, ad_params)
        b = StationResult(None, rotor_settings, rotor_settings, ad_params)
        c = StationResult(station, None, rotor_settings, ad_params)
        d = StationResult(station, rotor_settings, rotor_settings, ad_params)

        assert a != b != c
        assert hash(a) != hash(b) != hash(c)
        assert a is not b is not c

        assert a == d
