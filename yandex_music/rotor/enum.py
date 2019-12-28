from typing import TYPE_CHECKING, Optional, List

if TYPE_CHECKING:
    from yandex_music import Client, Value

from yandex_music import YandexMusicObject


class Enum(YandexMusicObject):
    def __init__(self,
                 type_: str,
                 name: str,
                 possible_values: List['Value'],
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        self.type = type_
        self.name = name
        self.possible_values = possible_values

        self.client = client
        self._id_attrs = (self.type, self.name, self.possible_values)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Enum']:
        if not data:
            return None

        data = super(Enum, cls).de_json(data, client)
        from yandex_music import Value
        data['possible_values'] = Value.de_list(data.get('possible_values'), client)

        return cls(client=client, **data)
