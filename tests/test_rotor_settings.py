from typing import Dict

from yandex_music import Client, JSONType, RotorSettings


class TestRotorSettings:
    language = 'not-russian'
    diversity = 'default'
    mood = 2
    energy = 2
    mood_energy = 'fun'

    def test_expected_values(self, rotor_settings: RotorSettings) -> None:
        assert rotor_settings.language == self.language
        assert rotor_settings.diversity == self.diversity
        assert rotor_settings.mood == self.mood
        assert rotor_settings.energy == self.energy
        assert rotor_settings.mood_energy == self.mood_energy

    def test_de_json_none(self, client: Client) -> None:
        assert RotorSettings.de_json({}, client) is None

    def test_de_json_required(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {'language': self.language, 'diversity': self.diversity}
        rotor_settings = RotorSettings.de_json(json_dict, client)
        assert rotor_settings is not None

        assert rotor_settings.language == self.language
        assert rotor_settings.diversity == self.diversity

    def test_de_json_all(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {
            'language': self.language,
            'diversity': self.diversity,
            'mood': self.mood,
            'energy': self.energy,
            'mood_energy': self.mood_energy,
        }
        rotor_settings = RotorSettings.de_json(json_dict, client)
        assert rotor_settings is not None

        assert rotor_settings.language == self.language
        assert rotor_settings.diversity == self.diversity
        assert rotor_settings.mood == self.mood
        assert rotor_settings.energy == self.energy
        assert rotor_settings.mood_energy == self.mood_energy

    def test_equality(self) -> None:
        a = RotorSettings(self.language, self.diversity)
        b = RotorSettings('', self.diversity)
        c = RotorSettings(self.language, self.diversity)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
