from dataclasses import field
from typing import TYPE_CHECKING, Iterator, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import (
        ClientType,
        JSONType,
        MetatagArtistEntry,
        MetatagSortByValue,
        MetatagTitle,
        Pager,
    )


@model
class MetatagArtists(YandexMusicModel):
    """Класс, представляющий страницу списка артистов метатега.

    Attributes:
        id (:obj:`str`, optional): Уникальный идентификатор метатега.
        cover_uri (:obj:`str`, optional): Ссылка на обложку.
        color (:obj:`str`, optional): Цвет оформления.
        title (:obj:`yandex_music.MetatagTitle`, optional): Заголовок метатега.
        station_id (:obj:`str`, optional): Идентификатор радиостанции.
        pager (:obj:`yandex_music.Pager`, optional): Пагинатор.
        artists (:obj:`list` из :obj:`yandex_music.MetatagArtistEntry`): Артисты метатега с популярными треками.
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
    artists: List['MetatagArtistEntry'] = field(default_factory=list)
    sort_by_values: List['MetatagSortByValue'] = field(default_factory=list)
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.id, self.pager, self.artists)

    def __getitem__(self, item: int) -> 'MetatagArtistEntry':
        return self.artists[item]

    def __iter__(self) -> Iterator['MetatagArtistEntry']:
        return iter(self.artists)

    def __len__(self) -> int:
        return len(self.artists)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['MetatagArtists']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.MetatagArtists`: Страница списка артистов метатега.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music import MetatagArtistEntry, MetatagSortByValue, MetatagTitle, Pager

        cls_data['title'] = MetatagTitle.de_json(cls_data.get('title'), client)
        cls_data['pager'] = Pager.de_json(cls_data.get('pager'), client)
        cls_data['artists'] = MetatagArtistEntry.de_list(cls_data.get('artists'), client)
        cls_data['sort_by_values'] = MetatagSortByValue.de_list(cls_data.get('sort_by_values'), client)

        return cls(client=client, **cls_data)
