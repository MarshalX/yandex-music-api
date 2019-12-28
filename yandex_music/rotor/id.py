from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from yandex_music import Client

from yandex_music import YandexMusicObject


class Id(YandexMusicObject):
    def __init__(self,
                 type_: str,
                 tag: str,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        self.type = type_
        self.tag = tag

        self.client = client
        self._id_attrs = (self.type, self.tag)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Id']:
        if not data:
            return None

        data = super(Id, cls).de_json(data, client)

        return cls(client=client, **data)
