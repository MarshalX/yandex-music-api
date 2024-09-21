from typing import TYPE_CHECKING, Optional, Union

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Chart, ClientType, JSONType, Track


@model
class TrackShort(YandexMusicModel):
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
        original_index (:obj:`int`, optional): Индекс в плейлисте или альбоме. TODO уточнить про альбом.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    id: Union[str, int]
    timestamp: str
    album_id: Optional[str] = None
    play_count: Optional[int] = None
    recent: Optional[bool] = None
    chart: Optional['Chart'] = None
    track: Optional['Track'] = None
    original_index: Optional[int] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.id, self.album_id)

    def fetch_track(self) -> 'Track':
        """Получение полной версии трека.

        Returns:
            :obj:`yandex_music.Track`: Полная версия трека.
        """
        assert self.valid_client(self.client)
        return self.client.tracks(self.track_id)[0]

    async def fetch_track_async(self) -> 'Track':
        """Получение полной версии трека.

        Returns:
            :obj:`yandex_music.Track`: Полная версия трека.
        """
        assert self.valid_async_client(self.client)
        return (await self.client.tracks(self.track_id))[0]

    @property
    def track_id(self) -> str:
        """:obj:`str`: Уникальный идентификатор трека состоящий из его номера и номера альбома или просто из номера."""
        if self.album_id:
            return f'{self.id}:{self.album_id}'

        return f'{self.id}'

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['TrackShort']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.TrackShort`: Укороченная версия трека с неполными данными.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music import Chart, Track

        cls_data['track'] = Track.de_json(data.get('track'), client)
        cls_data['chart'] = Chart.de_json(data.get('chart'), client)

        return cls(client=client, **cls_data)  # type: ignore

    # camelCase псевдонимы

    #: Псевдоним для :attr:`fetch_track`
    fetchTrack = fetch_track
    #: Псевдоним для :attr:`fetch_track_async`
    fetchTrackAsync = fetch_track_async
    #: Псевдоним для :attr:`track_id`
    trackId = track_id
