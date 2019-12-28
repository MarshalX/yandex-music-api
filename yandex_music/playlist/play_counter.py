from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from yandex_music import Client

from yandex_music import YandexMusicObject


class PlayCounter(YandexMusicObject):
    def __init__(self,
                 value: int,
                 description: str,
                 updated: bool,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        self.value = value
        self.description = description
        self.updated = updated

        self.client = client
        self._id_attrs = (self.value, self.description, self.updated)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['PlayCounter']:
        if not data:
            return None

        data = super(PlayCounter, cls).de_json(data, client)

        return cls(client=client, **data)
