from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, Event, JSONType, Track, TrackWithAds


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

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['Day']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Day`: День в фиде.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music import Event, Track, TrackWithAds

        cls_data['events'] = Event.de_list(data.get('events'), client)
        cls_data['tracks_to_play_with_ads'] = TrackWithAds.de_list(data.get('tracks_to_play_with_ads'), client)
        cls_data['tracks_to_play'] = Track.de_list(data.get('tracks_to_play'), client)

        return cls(client=client, **cls_data)  # type: ignore
