from dataclasses import field
from typing import TYPE_CHECKING, Iterator, List, Optional

from typing_extensions import override

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import (
        ClientType,
        MetatagSortByValue,
        MetatagTitle,
        Pager,
        Playlist,
    )


@model
class MetatagPlaylists(YandexMusicModel):
    """Класс, представляющий страницу списка плейлистов метатега.

    Attributes:
        id (:obj:`str`, optional): Уникальный идентификатор метатега.
        cover_uri (:obj:`str`, optional): Ссылка на обложку.
        color (:obj:`str`, optional): Цвет оформления.
        title (:obj:`yandex_music.MetatagTitle`, optional): Заголовок метатега.
        station_id (:obj:`str`, optional): Идентификатор радиостанции.
        pager (:obj:`yandex_music.Pager`, optional): Пагинатор.
        playlists (:obj:`list` из :obj:`yandex_music.Playlist`): Плейлисты метатега.
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
    playlists: List['Playlist'] = field(default_factory=list)
    sort_by_values: List['MetatagSortByValue'] = field(default_factory=list)
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.id, self.pager, self.playlists)

    @override
    def __getitem__(self, item: int) -> 'Playlist':
        return self.playlists[item]

    def __iter__(self) -> Iterator['Playlist']:
        return iter(self.playlists)

    def __len__(self) -> int:
        return len(self.playlists)
