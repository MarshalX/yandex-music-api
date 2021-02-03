from yandex_music import Restrictions


class TestRestrictions:
    def test_expected_values(self, restrictions, enum, discrete_scale):
        assert restrictions.language == enum
        assert restrictions.diversity == enum
        assert restrictions.mood == discrete_scale
        assert restrictions.energy == discrete_scale
        assert restrictions.mood_energy == enum

    def test_de_json_none(self, client):
        assert Restrictions.de_json({}, client) is None

    def test_de_json_required(self, client, enum):
        json_dict = {'language': enum.to_dict(), 'diversity': enum.to_dict()}
        restrictions = Restrictions.de_json(json_dict, client)

        assert restrictions.language == enum
        assert restrictions.diversity == enum

    def test_de_json_all(self, client, enum, discrete_scale):
        json_dict = {
            'language': enum.to_dict(),
            'diversity': enum.to_dict(),
            'mood': discrete_scale.to_dict(),
            'energy': discrete_scale.to_dict(),
            'mood_energy': enum.to_dict(),
        }
        restrictions = Restrictions.de_json(json_dict, client)

        assert restrictions.language == enum
        assert restrictions.diversity == enum
        assert restrictions.mood == discrete_scale
        assert restrictions.energy == discrete_scale
        assert restrictions.mood_energy == enum

    def test_equality(self, enum, discrete_scale):
        a = Restrictions(enum, enum)
        b = Restrictions(enum, None)
        c = Restrictions(enum, enum)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
