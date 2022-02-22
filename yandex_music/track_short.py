from typing import TYPE_CHECKING, Optional, List, Union

from yandex_music.utils import model
from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client, Track, Chart


@model
class TrackShort(YandexMusicObject):
    """Класс, представляющий укороченную версию трека с неполными данными.

    Note:
        Поля `chart` и `track` только у треков, полученных через метод `chart()`.

    Attributes:
        id (:obj:`str`): Уникальный идентификатор трека.
        timestamp (:obj:`str`): Дата TODO.
        album_id (:obj:`str`, optional): Уникальный идентификатор альбома.
        play_count (:obj:`int`, optional): Количество проигрываний.
        recent (:obj:`bool`, optional): Недавний.
        chart (:obj:`yandex_music.Chart`, optional): Позиция в чарте.
        track (:obj:`yandex_music.Track`, optional): Полная версия трека.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    id: Union[str, int]
    timestamp: str
    album_id: Optional[str] = None
    play_count: Optional[int] = None
    recent: Optional[bool] = None
    chart: Optional['Chart'] = None
    track: Optional['Track'] = None
    client: Optional['Client'] = None

    def __post_init__(self):
        self._id_attrs = (self.id, self.album_id)

    def fetch_track(self) -> 'Track':
        """Получение полной версии трека.

        Returns:
            :obj:`yandex_music.Track`: Полная версия трека.
        """
        return self.client.tracks(self.track_id)[0]

    async def fetch_track_async(self) -> 'Track':
        """Получение полной версии трека.

        Returns:
            :obj:`yandex_music.Track`: Полная версия трека.
        """
        return (await self.client.tracks(self.track_id))[0]

    @property
    def track_id(self) -> str:
        """:obj:`str`: Уникальный идентификатор трека состоящий из его номера и номера альбома или просто из номера."""
        if self.album_id:
            return f'{self.id}:{self.album_id}'

        return f'{self.id}'

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['TrackShort']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.TrackShort`: Укороченная версия трека с неполными данными.
        """
        if not data:
            return None

        data = super(TrackShort, cls).de_json(data, client)
        from yandex_music import Track, Chart

        data['track'] = Track.de_json(data.get('track'), client)
        data['chart'] = Chart.de_json(data.get('chart'), client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data: dict, client: 'Client') -> List['TrackShort']:
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.TrackShort`: Укороченные версии треков с неполными данными.
        """
        if not data:
            return []

        return [cls.de_json(track, client) for track in data]

    # camelCase псевдонимы

    #: Псевдоним для :attr:`fetch_track`
    fetchTrack = fetch_track
    #: Псевдоним для :attr:`fetch_track_async`
    fetchTrackAsync = fetch_track_async
    #: Псевдоним для :attr:`track_id`
    trackId = track_id
