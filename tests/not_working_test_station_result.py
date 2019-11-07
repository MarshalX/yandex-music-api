import pytest

from yandex_music import StationResult


@pytest.fixture(scope='class')
def station_result(station, settings, settings2, ad_params):
    return StationResult(station, settings, settings2, ad_params, TestStationResult.explanation,
                         TestStationResult.prerolls)


class TestStationResult:
    explanation = None
    prerolls = None

    def test_expected_values(self, station_result, station, settings, settings2, ad_params):
        assert station_result.station == station
        assert station_result.settings == settings
        assert station_result.settings2 == settings2
        assert station_result.ad_params == ad_params
        assert station_result.explanation == self.explanation
        assert station_result.prerolls == self.prerolls

    def test_de_json_required(self, client, station, settings, settings2, ad_params):
        json_dict = {'station': station, 'settings': settings, 'settings2': settings2, 'ad_params': ad_params}
        station_result = StationResult.de_json(json_dict, client)

        assert station_result.station == station
        assert station_result.settings == settings
        assert station_result.settings2 == settings2
        assert station_result.ad_params == ad_params

    def test_de_json_all(self, client, station, settings, settings2, ad_params):
        json_dict = {'station': station, 'settings': settings, 'settings2': settings2, 'ad_params': ad_params,
                     'explanation': self.explanation, 'prerolls': self.prerolls}
        station_result = StationResult.de_json(json_dict, client)

        assert station_result.station == station
        assert station_result.settings == settings
        assert station_result.settings2 == settings2
        assert station_result.ad_params == ad_params
        assert station_result.explanation == self.explanation
        assert station_result.prerolls == self.prerolls

    def test_equality(self):
        pass
