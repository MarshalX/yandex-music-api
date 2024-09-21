from typing import TYPE_CHECKING, Any, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, Track


@model
class TrackId(YandexMusicModel):
    """Класс, представляющий уникальный идентификатор трека.

    Note:
        Поле `track_id` используется только у объектах полученных через очередь треков. В остальные случаях `id`.

        Поле `from_` есть только у объект, которые используются в очереди треков.

    Attributes:
        id (:obj:`int`): Уникальный идентификатор трека.
        track_id (:obj:`int`): Уникальный идентификатор трека.
        album_id (:obj:`int`, optional): Уникальный идентификатор альбома.
        from_ (:obj:`str`, optional): Откуда был получен этот объект.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    id: Optional[int] = None
    track_id: Optional[int] = None
    album_id: Optional[int] = None
    from_: Optional[str] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.track_id, self.id, self.album_id)

    @property
    def track_full_id(self) -> str:
        """:obj:`str`: ID трека состоящий из его номера и номера альбома."""
        track_id = self.id
        if self.track_id:
            track_id = self.track_id

        return f'{track_id}:{self.album_id}'

    def fetch_track(self, *args: Any, **kwargs: Any) -> 'Track':
        """Получение полной версии трека.

        Returns:
            :obj:`yandex_music.Track`: Полная версия.
        """
        return self.client.tracks(self.track_full_id, *args, **kwargs)[0]

    async def fetch_track_async(self, *args: Any, **kwargs: Any) -> 'Track':
        """Получение полной версии трека.

        Returns:
            :obj:`yandex_music.Track`: Полная версия.
        """
        return (await self.client.tracks(self.track_full_id, *args, **kwargs))[0]

    # camelCase псевдонимы

    #: Псевдоним для :attr:`track_full_id`
    trackFullId = track_full_id
    #: Псевдоним для :attr:`fetch_track`
    fetchTrack = fetch_track
    #: Псевдоним для :attr:`fetch_track_async`
    fetchTrackAsync = fetch_track_async
