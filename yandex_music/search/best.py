from typing import TYPE_CHECKING, Optional, Union

from yandex_music import YandexMusicObject, Artist, Album, Track, Playlist, Video, User
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client


de_json_result = {
    'track': Track.de_json,
    'artist': Artist.de_json,
    'album': Album.de_json,
    'playlist': Playlist.de_json,
    'video': Video.de_json,
    'user': User.de_json,
    'podcast': Album.de_json,
    'podcast_episode': Track.de_json,
}


@model
class Best(YandexMusicObject):
    """Класс, представляющий лучший результат поиска.

    Attributes:
        type (:obj:`str`): Тип лучшего результата.
        result (:obj:`yandex_music.Track` | :obj:`yandex_music.Artist` | :obj:`yandex_music.Album` \
            | :obj:`yandex_music.Playlist` | :obj:`yandex_music.Video`): Лучший результат.
        text (:obj:`str`, optional): TODO.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    type: str
    result: Optional[Union[Track, Artist, Album, Playlist, Video]]
    text: Optional[str] = None
    client: Optional['Client'] = None

    def __post_init__(self):
        self._id_attrs = (self.type, self.result)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Best']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Best`: Лучший результат.
        """
        if not data:
            return None

        data = super(Best, cls).de_json(data, client)
        data['result'] = de_json_result.get(data.get('type'))(data.get('result'), client)

        return cls(client=client, **data)
