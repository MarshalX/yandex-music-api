from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, Track


@model
class PlaylistRecommendations(YandexMusicModel):
    """Класс, представляющий рекомендации для плейлиста.

    Attributes:
        tracks (:obj:`list` из :obj:`yandex_music.Track`): Список рекомендованных треков.
        batch_id (:obj:`str`, optional): Уникальный идентификатор партии треков.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    tracks: List['Track']
    batch_id: Optional[str] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.batch_id, self.tracks)
