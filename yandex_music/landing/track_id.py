from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from yandex_music import Client

from yandex_music import YandexMusicObject


class TrackId(YandexMusicObject):
    def __init__(self,
                 id_: int,
                 album_id: Optional[int] = None,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        self.id = id_

        self.album_id = album_id
        self.client = client
        self._id_attrs = (self.id, self.album_id)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['TrackId']:
        if not data:
            return None

        data = super(TrackId, cls).de_json(data, client)

        return cls(client=client, **data)
