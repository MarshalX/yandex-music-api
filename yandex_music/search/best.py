from typing import TYPE_CHECKING, Optional, Union

if TYPE_CHECKING:
    from yandex_music import Client

from yandex_music import YandexMusicObject, Artist, Album, Track, Playlist, Video


de_json_result = {
    'track': Track.de_json,
    'artist': Artist.de_json,
    'album': Album.de_json,
    'playlist': Playlist.de_json,
    'video': Video.de_json,
}


class Best(YandexMusicObject):
    def __init__(self,
                 type_: str,
                 result: Optional[Union[Track, Artist, Album, Playlist, Video]],
                 text: Optional[str] = None,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        self.type = type_
        self.result = result

        self.text = text

        self.client = client
        self._id_attrs = (self.type, self.result)

    @classmethod
    def de_json(cls, data: dict, client: 'Client'):
        if not data:
            return None

        data = super(Best, cls).de_json(data, client)
        data['result'] = de_json_result.get(data.get('type_'))(data.get('result'), client)

        return cls(client=client, **data)
