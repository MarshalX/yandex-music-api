from typing import TYPE_CHECKING, Optional, Union

from yandex_music import Album, Artist, Playlist, Track, User, Video, YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType, MapTypeToDeJson


_TYPE_TO_DE_JSON_DEF: 'MapTypeToDeJson' = {
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
class Best(YandexMusicModel):
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
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.type, self.result)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['Best']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Best`: Лучший результат.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)

        type_ = data.get('type')
        if type_ and type_ in _TYPE_TO_DE_JSON_DEF:
            de_json = _TYPE_TO_DE_JSON_DEF[type_]
            cls_data['result'] = de_json(data.get('result'), client)

        return cls(client=client, **cls_data)  # type: ignore
