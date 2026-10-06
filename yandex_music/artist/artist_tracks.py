from typing import TYPE_CHECKING, Iterator, List, Optional

from typing_extensions import override

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, Pager, Track


@model
class ArtistTracks(YandexMusicModel):
    """Класс, представляющий страницу списка треков артиста.

    Attributes:
        tracks (:obj:`list` из :obj:`yandex_music.Track`): Список треков артиста.
        pager (:obj:`yandex_music.Pager`): Пагинатор.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    tracks: List['Track']
    pager: Optional['Pager']
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.pager, self.tracks)

    @override
    def __getitem__(self, item: int) -> 'Track':
        return self.tracks[item]

    def __iter__(self) -> Iterator['Track']:
        return iter(self.tracks)

    def __len__(self) -> int:
        return len(self.tracks)
