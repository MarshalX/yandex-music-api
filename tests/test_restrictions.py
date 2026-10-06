from typing import Dict

from yandex_music import Client, DiscreteScale, Enum, JSONType, Restrictions


class TestRestrictions:
    def test_expected_values(self, restrictions: Restrictions, enum: Enum, discrete_scale: DiscreteScale) -> None:
        assert restrictions.language == enum
        assert restrictions.diversity == enum
        assert restrictions.mood == discrete_scale
        assert restrictions.energy == discrete_scale
        assert restrictions.mood_energy == enum

    def test_de_json_none(self, client: Client) -> None:
        assert Restrictions.de_json({}, client) is None

    def test_de_json_required(self, client: Client, enum: Enum) -> None:
        json_dict: Dict[str, JSONType] = {'language': enum.to_dict(), 'diversity': enum.to_dict()}
        restrictions = Restrictions.de_json(json_dict, client)
        assert restrictions is not None

        assert restrictions.language == enum
        assert restrictions.diversity == enum

    def test_de_json_all(self, client: Client, enum: Enum, discrete_scale: DiscreteScale) -> None:
        json_dict: Dict[str, JSONType] = {
            'language': enum.to_dict(),
            'diversity': enum.to_dict(),
            'mood': discrete_scale.to_dict(),
            'energy': discrete_scale.to_dict(),
            'mood_energy': enum.to_dict(),
        }
        restrictions = Restrictions.de_json(json_dict, client)
        assert restrictions is not None

        assert restrictions.language == enum
        assert restrictions.diversity == enum
        assert restrictions.mood == discrete_scale
        assert restrictions.energy == discrete_scale
        assert restrictions.mood_energy == enum

    def test_equality(self, enum: Enum) -> None:
        a = Restrictions(enum, enum)
        b = Restrictions(enum, None)
        c = Restrictions(enum, enum)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
