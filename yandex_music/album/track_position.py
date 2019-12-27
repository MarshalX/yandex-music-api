from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from yandex_music import Client

from yandex_music import YandexMusicObject


class TrackPosition(YandexMusicObject):
    def __init__(self,
                 volume,
                 index,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        self.volume = volume
        self.index = index

        self.client = client
        self._id_attrs = (self.volume, self.index)

    @classmethod
    def de_json(cls, data: dict, client: 'Client'):
        if not data:
            return None

        data = super(TrackPosition, cls).de_json(data, client)

        return cls(client=client, **data)
