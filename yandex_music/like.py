from typing import List, Optional, TYPE_CHECKING

from yandex_music import Album, Artist, Playlist, YandexMusicObject
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client

de_list = {
    'album': Album.de_json,
    'playlist': Playlist.de_json,
}


@model
class Like(YandexMusicObject):
    """Класс, представляющий объект с отметкой "мне нравится".

    None:
        В поле `type` содержится одно из трёх значений: `artist`, `playlist`, `album`. Обозначает поле, в котором
        содержится информация.

    Attributes:
        type (:obj:`str`): Тип объекта с отметкой.
        id (:obj:`str`, optional): Уникальный идентификатор отметки.
        timestamp (:obj:`str`, optional): Дата и время добавления отметки.
        album (:obj:`yandex_music.Album`, optional): Понравившейся альбом.
        artist (:obj:`yandex_music.Artist`, optional): Понравившейся артист.
        playlist (:obj:`yandex_music.Playlist`, optional): Понравившейся плейлист.
        short_description (:obj:`str`, optional): Короткое описание.
        description (:obj:`str`, optional): Описание.
        is_premiere (:obj:`bool`, optional): Премьера ли.
        is_banner (:obj:`bool`, optional): Является ли баннером.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    type: str
    id: Optional[str] = None
    timestamp: Optional[str] = None
    album: Optional['Album'] = None
    artist: Optional['Artist'] = None
    playlist: Optional['Playlist'] = None
    short_description: Optional[str] = None
    description: Optional[str] = None
    is_premiere: Optional[bool] = None
    is_banner: Optional[bool] = None
    client: Optional['Client'] = None

    def __post_init__(self):
        self._id_attrs = (self.id, self.type, self.timestamp, self.album, self.artist, self.playlist)

    @classmethod
    def de_json(cls, data: dict, client: 'Client', type_: str = None) -> Optional['Like']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            type_ (:obj:`str`, optional): Тип объекта с отметкой "мне нравится".
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Like`: Объект с отметкой "мне нравится".
        """
        if not data:
            return None

        data = super(Like, cls).de_json(data, client)

        if type_ == 'artist':
            if 'artist' not in data:
                temp_data = data.copy()
                data.clear()
                data[type_] = Artist.de_json(temp_data, client)
            else:
                data[type_] = Artist.de_json(data.get('artist'), client)
        else:
            data[type_] = de_list[type_](data.get(type_), client)

        data['type'] = type_

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data: dict, client: 'Client', type_: str = None) -> List['Like']:
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            type_ (:obj:`str`, optional): Тип объекта с отметкой "мне нравится".
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.Like`: Объекты с отметкой "мне нравится".
        """
        if not data:
            return []

        likes = list()
        for like in data:
            likes.append(cls.de_json(like, client, type_))

        return likes
