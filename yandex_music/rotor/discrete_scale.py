from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from yandex_music import Client, Value

from yandex_music import YandexMusicObject


class DiscreteScale(YandexMusicObject):
    def __init__(self,
                 type_: str,
                 name: str,
                 min_: Optional['Value'],
                 max_: Optional['Value'],
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        self.type = type_
        self.name = name
        self.min = min_
        self.max = max_

        self.client = client
        self._id_attrs = (self.type, self.name, self.min, self.max)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['DiscreteScale']:
        if not data:
            return None

        data = super(DiscreteScale, cls).de_json(data, client)
        from yandex_music import Value
        data['min_'] = Value.de_json(data.get('min_'), client)
        data['max_'] = Value.de_json(data.get('max_'), client)

        return cls(client=client, **data)
