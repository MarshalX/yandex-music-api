from typing import TYPE_CHECKING, Optional, List

if TYPE_CHECKING:
    from yandex_music import Client

from yandex_music import YandexMusicObject


class Value(YandexMusicObject):
    def __init__(self,
                 value: str,
                 name: str,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        self.value = value
        self.name = name

        self.client = client
        self._id_attrs = (self.value, self.name)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Value']:
        if not data:
            return None

        data = super(Value, cls).de_json(data, client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data: dict, client: 'Client') -> List['Value']:
        if not data:
            return []

        values = list()
        for value in data:
            values.append(cls.de_json(value, client))

        return values
