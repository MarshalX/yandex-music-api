from typing import Dict

from yandex_music import Client, JSONType, Restrictions, WaveDefaultStation, WaveSettings, WaveSettingsBlock


class TestWaveSettings:
    def test_expected_values(
        self,
        wave_settings: WaveSettings,
        wave_default_station: WaveDefaultStation,
        wave_settings_block: WaveSettingsBlock,
        restrictions: Restrictions,
    ) -> None:
        assert wave_settings.default_station == wave_default_station
        assert wave_settings.blocks == [wave_settings_block]
        assert wave_settings.setting_restrictions == restrictions

    def test_de_json_none(self, client: Client) -> None:
        assert WaveSettings.de_json({}, client) is None

    def test_de_json_all(
        self,
        client: Client,
        wave_default_station: WaveDefaultStation,
        wave_settings_block: WaveSettingsBlock,
        restrictions: Restrictions,
    ) -> None:
        json_dict: Dict[str, JSONType] = {
            'defaultStation': wave_default_station.to_dict(),
            'blocks': [wave_settings_block.to_dict()],
            'settingRestrictions': restrictions.to_dict(),
        }
        wave_settings = WaveSettings.de_json(json_dict, client)
        assert wave_settings is not None

        assert wave_settings.default_station == wave_default_station
        assert wave_settings.blocks == [wave_settings_block]
        assert wave_settings.setting_restrictions == restrictions

    def test_equality(
        self,
        wave_default_station: WaveDefaultStation,
        wave_settings_block: WaveSettingsBlock,
        restrictions: Restrictions,
    ) -> None:
        a = WaveSettings(wave_default_station, [wave_settings_block], restrictions)
        b = WaveSettings(wave_default_station, [], restrictions)
        c = WaveSettings(wave_default_station, [wave_settings_block], restrictions)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
