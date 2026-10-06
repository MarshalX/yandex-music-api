from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, Event, Track, TrackWithAds


@model
class Day(YandexMusicModel):
    """Класс, представляющий день в фиде.

    Attributes:
        day (:obj:`str`): Дата в формате YYYY-MM-DD.
        events (:obj:`list` из :obj:`yandex_music.Event`): События TODO.
        tracks_to_play_with_ads (:obj:`list` из :obj:`yandex_music.TrackWithAds`): Треки для проигрывания с рекламой.
        tracks_to_play (:obj:`list` из :obj:`yandex_music.Track`): Треки для проигрывания.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    day: str
    events: List['Event']
    tracks_to_play_with_ads: List['TrackWithAds']
    tracks_to_play: List['Track']
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.day, self.events, self.tracks_to_play_with_ads, self.tracks_to_play)
