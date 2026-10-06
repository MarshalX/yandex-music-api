from typing import TYPE_CHECKING, Iterator, List, Optional

from typing_extensions import override

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Artist, ClientType, Pager


@model
class LabelArtists(YandexMusicModel):
    """Класс, представляющий страницу списка артистов лейбла.

    Attributes:
        artists (:obj:`list` из :obj:`yandex_music.Artist`): Список артистов лейбла.
        pager (:obj:`yandex_music.Pager`, optional): Пагинатор.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    artists: List['Artist']
    pager: Optional['Pager']
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.pager, self.artists)

    @override
    def __getitem__(self, item: int) -> 'Artist':
        return self.artists[item]

    def __iter__(self) -> Iterator['Artist']:
        return iter(self.artists)

    def __len__(self) -> int:
        return len(self.artists)
