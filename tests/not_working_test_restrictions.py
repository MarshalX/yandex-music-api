from yandex_music import Restrictions


class TestRestrictions:
    language = None
    diversity = None
    mood = None
    energy = None
    mood_energy = None

    def test_expected_values(self, restrictions):
        assert restrictions.language == self.language
        assert restrictions.diversity == self.diversity
        assert restrictions.mood == self.mood
        assert restrictions.energy == self.energy
        assert restrictions.mood_energy == self.mood_energy

    def test_de_json_required(self, client):
        json_dict = {'language': self.language, 'diversity': self.diversity}
        restrictions = Restrictions.de_json(json_dict, client)

        assert restrictions.language == self.language
        assert restrictions.diversity == self.diversity

    def test_de_json_all(self, client):
        json_dict = {'language': self.language, 'diversity': self.diversity, 'mood': self.mood, 'energy': self.energy,
                     'mood_energy': self.mood_energy}
        restrictions = Restrictions.de_json(json_dict, client)

        assert restrictions.language == self.language
        assert restrictions.diversity == self.diversity
        assert restrictions.mood == self.mood
        assert restrictions.energy == self.energy
        assert restrictions.mood_energy == self.mood_energy

    def test_equality(self):
        pass
