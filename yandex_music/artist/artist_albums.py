from typing import TYPE_CHECKING, Iterator, List, Optional

from typing_extensions import override

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Album, ClientType, Pager


@model
class ArtistAlbums(YandexMusicModel):
    """Класс, представляющий страницу списка альбомов артиста.

    Attributes:
        albums (:obj:`list` из :obj:`yandex_music.Album`): Список альбомов артиста.
        pager (:obj:`yandex_music.Pager`): Пагинатор.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    albums: List['Album']
    pager: Optional['Pager']
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.pager, self.albums)

    @override
    def __getitem__(self, item: int) -> 'Album':
        return self.albums[item]

    def __iter__(self) -> Iterator['Album']:
        return iter(self.albums)

    def __len__(self) -> int:
        return len(self.albums)
