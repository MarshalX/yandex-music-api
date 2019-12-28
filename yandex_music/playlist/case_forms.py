from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from yandex_music import Client

from yandex_music import YandexMusicObject


class CaseForms(YandexMusicObject):
    def __init__(self,
                 nominative: str,
                 genitive: str,
                 dative: str,
                 accusative: str,
                 instrumental: str,
                 prepositional: str,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        self.nominative = nominative
        self.genitive = genitive
        self.dative = dative
        self.accusative = accusative
        self.instrumental = instrumental
        self.prepositional = prepositional

        self.client = client
        self._id_attrs = (self.nominative, self.genitive, self.dative,
                          self.accusative, self.instrumental, self.prepositional)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['CaseForms']:
        if not data:
            return None

        data = super(CaseForms, cls).de_json(data, client)

        return cls(client=client, **data)
