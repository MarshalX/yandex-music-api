from typing import TYPE_CHECKING, Iterator, List, Optional

from typing_extensions import override

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, Track


@model
class SimilarTracks(YandexMusicModel):
    """Класс, представляющий список похожих треков на другой трек.

    Attributes:
        track (:obj:`yandex_music.Track`): Трек.
        similar_tracks (:obj:`list` из :obj:`yandex_music.Track`): Похожие треки на `track`.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    track: Optional['Track']
    similar_tracks: List['Track']
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.track, self.similar_tracks)

    @override
    def __getitem__(self, item: int) -> 'Track':
        return self.similar_tracks[item]

    def __iter__(self) -> Iterator['Track']:
        return iter(self.similar_tracks)

    def __len__(self) -> int:
        return len(self.similar_tracks)
