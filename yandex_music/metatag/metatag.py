from dataclasses import field
from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import (
        Album,
        Artist,
        ClientType,
        JSONType,
        MetatagSortByValue,
        MetatagTitle,
        Playlist,
    )


@model
class Metatag(YandexMusicModel):
    """Класс, представляющий метатег.

    Note:
        Метатег объединяет артистов, альбомы и плейлисты по настроению, жанру, эпохе
        или занятию. Поле :attr:`station_id` позволяет запустить соответствующую радиостанцию.

    Warning:
        API также возвращает поля `tracks`, `composers` (как список артистов-композиторов),
        `promotions`, `features` и `concerts`, однако эти поля не описаны в библиотеке:
        `tracks`, `promotions`, `features` и `concerts` во всех опробованных метатегах возвращали
        пустой список, из-за чего структура их элементов достоверно неизвестна. При необходимости
        они могут быть добавлены в будущих версиях.

    Attributes:
        id (:obj:`str`, optional): Уникальный идентификатор метатега.
        cover_uri (:obj:`str`, optional): Ссылка на обложку.
        color (:obj:`str`, optional): Цвет оформления.
        title (:obj:`yandex_music.MetatagTitle`, optional): Заголовок метатега.
        liked (:obj:`bool`, optional): Отмечен ли метатег как понравившийся пользователем.
        station_id (:obj:`str`, optional): Идентификатор радиостанции.
        custom_wave_animation_url (:obj:`str`, optional): Ссылка на анимацию вайба.
        artists (:obj:`list` из :obj:`yandex_music.Artist`): Список артистов метатега.
        albums (:obj:`list` из :obj:`yandex_music.Album`): Список альбомов метатега.
        playlists (:obj:`list` из :obj:`yandex_music.Playlist`): Список плейлистов метатега.
        tracks_sort_by_values (:obj:`list` из :obj:`yandex_music.MetatagSortByValue`):
            Допустимые значения сортировки списка треков.
        albums_sort_by_values (:obj:`list` из :obj:`yandex_music.MetatagSortByValue`):
            Допустимые значения сортировки списка альбомов.
        playlists_sort_by_values (:obj:`list` из :obj:`yandex_music.MetatagSortByValue`):
            Допустимые значения сортировки списка плейлистов.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    id: Optional[str] = None
    cover_uri: Optional[str] = None
    color: Optional[str] = None
    title: Optional['MetatagTitle'] = None
    liked: Optional[bool] = None
    station_id: Optional[str] = None
    custom_wave_animation_url: Optional[str] = None
    artists: List['Artist'] = field(default_factory=list)
    albums: List['Album'] = field(default_factory=list)
    playlists: List['Playlist'] = field(default_factory=list)
    tracks_sort_by_values: List['MetatagSortByValue'] = field(default_factory=list)
    albums_sort_by_values: List['MetatagSortByValue'] = field(default_factory=list)
    playlists_sort_by_values: List['MetatagSortByValue'] = field(default_factory=list)
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.id,)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['Metatag']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Metatag`: Метатег.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music import Album, Artist, MetatagSortByValue, MetatagTitle, Playlist

        cls_data['title'] = MetatagTitle.de_json(cls_data.get('title'), client)
        cls_data['artists'] = Artist.de_list(cls_data.get('artists'), client)
        cls_data['albums'] = Album.de_list(cls_data.get('albums'), client)
        cls_data['playlists'] = Playlist.de_list(cls_data.get('playlists'), client)
        cls_data['tracks_sort_by_values'] = MetatagSortByValue.de_list(cls_data.get('tracks_sort_by_values'), client)
        cls_data['albums_sort_by_values'] = MetatagSortByValue.de_list(cls_data.get('albums_sort_by_values'), client)
        cls_data['playlists_sort_by_values'] = MetatagSortByValue.de_list(
            cls_data.get('playlists_sort_by_values'), client
        )

        return cls(client=client, **cls_data)
