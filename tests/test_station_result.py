from yandex_music import StationResult


class TestStationResult:
    explanation = ''
    prerolls = []
    rup_title = 'Моя волна'
    rup_description = 'Волна подстраивается под жанр и\xa0вас. Слушайте только то, что\xa0нравится!'
    custom_name = "R'n'B"

    def test_expected_values(self, station_result, station, rotor_settings, ad_params):
        assert station_result.station == station
        assert station_result.settings == rotor_settings
        assert station_result.settings2 == rotor_settings
        assert station_result.ad_params == ad_params
        assert station_result.explanation == self.explanation
        assert station_result.prerolls == self.prerolls
        assert station_result.rup_title == self.rup_title
        assert station_result.rup_description == self.rup_description
        assert station_result.custom_name == self.custom_name

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
            'rup_title': self.rup_title,
            'rup_description': self.rup_description,
        }
        station_result = StationResult.de_json(json_dict, client)

        assert station_result.station == station
        assert station_result.settings == rotor_settings
        assert station_result.settings2 == rotor_settings
        assert station_result.ad_params == ad_params
        assert station_result.rup_title == self.rup_title
        assert station_result.rup_description == self.rup_description

    def test_de_json_all(self, client, station, rotor_settings, ad_params):
        json_dict = {
            'station': station.to_dict(),
            'settings': rotor_settings.to_dict(),
            'settings2': rotor_settings.to_dict(),
            'ad_params': ad_params.to_dict(),
            'explanation': self.explanation,
            'prerolls': self.prerolls,
            'rup_title': self.rup_title,
            'rup_description': self.rup_description,
            'custom_name': self.custom_name,
        }
        station_result = StationResult.de_json(json_dict, client)

        assert station_result.station == station
        assert station_result.settings == rotor_settings
        assert station_result.settings2 == rotor_settings
        assert station_result.ad_params == ad_params
        assert station_result.explanation == self.explanation
        assert station_result.prerolls == self.prerolls
        assert station_result.rup_title == self.rup_title
        assert station_result.rup_description == self.rup_description
        assert station_result.custom_name == self.custom_name

    def test_equality(self, station, rotor_settings, ad_params):
        a = StationResult(station, rotor_settings, rotor_settings, ad_params)
        b = StationResult(None, rotor_settings, rotor_settings, ad_params)
        c = StationResult(station, None, rotor_settings, ad_params)
        d = StationResult(station, rotor_settings, rotor_settings, ad_params)

        assert a != b != c
        assert hash(a) != hash(b) != hash(c)
        assert a is not b is not c

        assert a == d
