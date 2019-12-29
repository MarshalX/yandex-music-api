from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from yandex_music import Client

from yandex_music import YandexMusicObject


class RotorSettings(YandexMusicObject):
    def __init__(self,
                 language: str,
                 diversity: str,
                 mood: Optional[int] = None,
                 energy: Optional[int] = None,
                 mood_energy=None,
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
    def de_json(cls, data: dict, client: 'Client') -> Optional['RotorSettings']:
        if not data:
            return None

        data = super(RotorSettings, cls).de_json(data, client)

        return cls(client=client, **data)
