from typing import TYPE_CHECKING, Optional, List

from yandex_music import YandexMusicObject
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client, Track


@model
class TrackWithAds(YandexMusicObject):
    """Класс, представляющий трек с рекламой.

    Note:
        Поле `type` встречалось только с значением `track`.

    Attributes:
        type (:obj:`str`): Тип TODO.
        track (:obj:`yandex_music.Track`): Трек.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    type: str
    track: Optional['Track']
    client: Optional['Client'] = None

    def __post_init__(self):
        self._id_attrs = (self.type, self.track)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['TrackWithAds']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.TrackWithAds`: Трек с рекламой.
        """
        if not data:
            return None

        data = super(TrackWithAds, cls).de_json(data, client)
        from yandex_music import Track

        data['track'] = Track.de_json(data.get('track'), client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data: dict, client: 'Client') -> List['TrackWithAds']:
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.TrackWithAds`: Треки с рекламой.
        """
        if not data:
            return []

        tracks_with_ads = list()
        for track_with_ads in data:
            tracks_with_ads.append(cls.de_json(track_with_ads, client))

        return tracks_with_ads
