from typing import TYPE_CHECKING, Optional, Sequence

from yandex_music import Album, Artist, Playlist, YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType, MapTypeToDeJson

_TYPE_TO_DE_JSON_DEF: 'MapTypeToDeJson' = {
    'album': Album.de_json,
    'playlist': Playlist.de_json,
}


@model
class Like(YandexMusicModel):
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
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.id, self.type, self.timestamp, self.album, self.artist, self.playlist)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType', type_: Optional[str] = None) -> Optional['Like']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
            type_ (:obj:`str`, optional): Тип объекта с отметкой "мне нравится".

        Returns:
            :obj:`yandex_music.Like`: Объект с отметкой "мне нравится".
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)

        if type_ == 'artist':
            if 'artist' not in data:
                temp_data = data.copy()
                cls_data.clear()
                cls_data[type_] = Artist.de_json(temp_data, client)
            else:
                cls_data[type_] = Artist.de_json(data.get('artist'), client)
        elif type_:
            de_json = _TYPE_TO_DE_JSON_DEF[type_]
            cls_data[type_] = de_json(data.get(type_), client)

        cls_data['type'] = type_

        return cls(client=client, **cls_data)  # type: ignore

    @classmethod
    def de_list(cls, data: JSONType, client: 'ClientType', type_: Optional[str] = None) -> Sequence['Like']:
        """Десериализация списка объектов.

        Note:
            Переопределяется в дочерних классах, если необходимо.

            Например, в сложных объектах где есть вариации подтипов.

        Args:
            data (:obj:`JSONType`): Список словарей с полями и значениями десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
            type_ (:obj:`str`, optional): Тип объекта с отметкой "мне нравится".

        Returns:
            :obj:`list` из :obj:`yandex_music.Like`: Список десериализованных объектов.
        """
        if not cls.is_array_model_data(data):
            return []

        items = [cls.de_json(item, client, type_) for item in data]
        return [item for item in items if item is not None]
