from typing import TYPE_CHECKING, Optional, Union

if TYPE_CHECKING:
    from yandex_music import Client

from yandex_music import YandexMusicObject, Enum, DiscreteScale


de_json = {
    'enum': Enum.de_json,
    'discrete-scale': DiscreteScale.de_json
}


class Restrictions(YandexMusicObject):
    def __init__(self,
                 language: Optional[Union['Enum', 'DiscreteScale']],
                 diversity: Optional[Union['Enum', 'DiscreteScale']],
                 mood: Optional[Union['Enum', 'DiscreteScale']] = None,
                 energy: Optional[Union['Enum', 'DiscreteScale']] = None,
                 mood_energy: Optional[Union['Enum', 'DiscreteScale']] = None,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        self.language = language
        self.diversity = diversity
        self.mood = mood
        self.energy = energy
        self.mood_energy = mood_energy

        self.client = client
        self._id_attrs = (self.language, self.diversity)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Restrictions']:
        if not data:
            return None

        data = super(Restrictions, cls).de_json(data, client)

        for key, value in data.items():
            data[key] = de_json.get(value.get('type_'))(value, client)

        return cls(client=client, **data)
