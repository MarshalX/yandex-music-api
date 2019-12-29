from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from yandex_music import Client

from yandex_music import YandexMusicObject


class Major(YandexMusicObject):
    def __init__(self,
                 id_: int,
                 name: str,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        self.id = id_
        self.name = name

        self.client = client
        self._id_attrs = (self.id, self.name)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Major']:
        if not data:
            return None

        data = super(Major, cls).de_json(data, client)

        return cls(client=client, **data)
