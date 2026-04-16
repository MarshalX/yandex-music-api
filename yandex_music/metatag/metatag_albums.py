from dataclasses import field
from typing import TYPE_CHECKING, Iterator, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import (
        Album,
        ClientType,
        JSONType,
        MetatagSortByValue,
        MetatagTitle,
        Pager,
    )


@model
class MetatagAlbums(YandexMusicModel):
    """Класс, представляющий страницу списка альбомов метатега.

    Attributes:
        id (:obj:`str`, optional): Уникальный идентификатор метатега.
        cover_uri (:obj:`str`, optional): Ссылка на обложку.
        color (:obj:`str`, optional): Цвет оформления.
        title (:obj:`yandex_music.MetatagTitle`, optional): Заголовок метатега.
        station_id (:obj:`str`, optional): Идентификатор радиостанции.
        pager (:obj:`yandex_music.Pager`, optional): Пагинатор.
        albums (:obj:`list` из :obj:`yandex_music.Album`): Альбомы метатега.
        sort_by_values (:obj:`list` из :obj:`yandex_music.MetatagSortByValue`):
            Допустимые значения сортировки.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    id: Optional[str] = None
    cover_uri: Optional[str] = None
    color: Optional[str] = None
    title: Optional['MetatagTitle'] = None
    station_id: Optional[str] = None
    pager: Optional['Pager'] = None
    albums: List['Album'] = field(default_factory=list)
    sort_by_values: List['MetatagSortByValue'] = field(default_factory=list)
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.id, self.pager, self.albums)

    def __getitem__(self, item: int) -> 'Album':
        return self.albums[item]

    def __iter__(self) -> Iterator['Album']:
        return iter(self.albums)

    def __len__(self) -> int:
        return len(self.albums)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['MetatagAlbums']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.MetatagAlbums`: Страница списка альбомов метатега.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music import Album, MetatagSortByValue, MetatagTitle, Pager

        cls_data['title'] = MetatagTitle.de_json(cls_data.get('title'), client)
        cls_data['pager'] = Pager.de_json(cls_data.get('pager'), client)
        cls_data['albums'] = Album.de_list(cls_data.get('albums'), client)
        cls_data['sort_by_values'] = MetatagSortByValue.de_list(cls_data.get('sort_by_values'), client)

        return cls(client=client, **cls_data)
