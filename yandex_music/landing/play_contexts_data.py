from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, TrackShortOld


@model
class PlayContextsData(YandexMusicModel):
    """Класс, представляющий данные проигрываемого контекста.

    Attributes:
        other_tracks (:obj:`list` из :obj:`yandex_music.TrackShortOld`): Другие треки.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    other_tracks: List['TrackShortOld']
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.other_tracks,)
