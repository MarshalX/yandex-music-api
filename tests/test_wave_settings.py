from yandex_music import WaveSettings


class TestWaveSettings:
    def test_expected_values(self, wave_settings, wave_default_station, wave_settings_block, restrictions):
        assert wave_settings.default_station == wave_default_station
        assert wave_settings.blocks == [wave_settings_block]
        assert wave_settings.setting_restrictions == restrictions

    def test_de_json_none(self, client):
        assert WaveSettings.de_json({}, client) is None

    def test_de_json_all(self, client, wave_default_station, wave_settings_block, restrictions):
        json_dict = {
            'defaultStation': wave_default_station.to_dict(),
            'blocks': [wave_settings_block.to_dict()],
            'settingRestrictions': restrictions.to_dict(),
        }
        wave_settings = WaveSettings.de_json(json_dict, client)

        assert wave_settings.default_station == wave_default_station
        assert wave_settings.blocks == [wave_settings_block]
        assert wave_settings.setting_restrictions == restrictions

    def test_equality(self, wave_default_station, wave_settings_block, restrictions):
        a = WaveSettings(wave_default_station, [wave_settings_block], restrictions)
        b = WaveSettings(wave_default_station, [], restrictions)
        c = WaveSettings(wave_default_station, [wave_settings_block], restrictions)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
