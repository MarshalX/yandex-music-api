import pytest

from yandex_music import RotorSettings


@pytest.fixture(scope='class')
def rotor_settings():
    return RotorSettings(TestRotorSettings.language, TestRotorSettings.diversity, TestRotorSettings.mood,
                         TestRotorSettings.energy, TestRotorSettings.mood_energy)


class TestRotorSettings:
    language = None
    diversity = None
    mood = None
    energy = None
    mood_energy = None

    def test_expected_values(self, rotor_settings):
        assert rotor_settings.language == self.language
        assert rotor_settings.diversity == self.diversity
        assert rotor_settings.mood == self.mood
        assert rotor_settings.energy == self.energy
        assert rotor_settings.mood_energy == self.mood_energy

    def test_de_json_required(self, client):
        json_dict = {'language': self.language, 'diversity': self.diversity}
        rotor_settings = RotorSettings.de_json(json_dict, client)

        assert rotor_settings.language == self.language
        assert rotor_settings.diversity == self.diversity

    def test_de_json_all(self, client):
        json_dict = {'language': self.language, 'diversity': self.diversity, 'mood': self.mood, 'energy': self.energy,
                     'mood_energy': self.mood_energy}
        rotor_settings = RotorSettings.de_json(json_dict, client)

        assert rotor_settings.language == self.language
        assert rotor_settings.diversity == self.diversity
        assert rotor_settings.mood == self.mood
        assert rotor_settings.energy == self.energy
        assert rotor_settings.mood_energy == self.mood_energy

    def test_equality(self):
        pass
