from typing import TYPE_CHECKING, Iterator, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType, Track, TrackShort


@model
class TracksList(YandexMusicModel):
    """Класс, представляющий список треков.

    Attributes:
        uid (:obj:`int`): Уникальный идентификатор пользователя.
        revision (:obj:`int`): Актуальность данных TODO.
        tracks (:obj:`list` из :obj:`yandex_music.TrackShort`): Список треков в укороченной версии.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    uid: int
    revision: int
    tracks: List['TrackShort']
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.uid, self.tracks)

    def __getitem__(self, item: int) -> 'TrackShort':
        return self.tracks[item]

    def __iter__(self) -> Iterator['TrackShort']:
        return iter(self.tracks)

    def __len__(self) -> int:
        return len(self.tracks)

    @property
    def tracks_ids(self) -> List[str]:
        """:obj:`list` из :obj:`str`: Список уникальных идентификаторов треков."""
        return [track.track_id for track in self.tracks]

    def fetch_tracks(self) -> List['Track']:
        """Получение полных версии треков.

        Returns:
            :obj:`list` из :obj:`yandex_music.Track`: Полная версия трека.
        """
        assert self.valid_client(self.client)
        return self.client.tracks(self.tracks_ids)

    async def fetch_tracks_async(self) -> List['Track']:
        """Получение полных версии треков.

        Returns:
            :obj:`list` из :obj:`yandex_music.Track`: Полная версия трека.
        """
        assert self.valid_async_client(self.client)
        return await self.client.tracks(self.tracks_ids)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['TracksList']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.TracksList`: Список треков.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music import TrackShort

        cls_data['tracks'] = TrackShort.de_list(data.get('tracks'), client)

        return cls(client=client, **cls_data)  # type: ignore

    # camelCase псевдонимы

    #: Псевдоним для :attr:`tracks_ids`
    tracksIds = tracks_ids
    #: Псевдоним для :attr:`fetch_tracks`
    fetchTracks = fetch_tracks
    #: Псевдоним для :attr:`fetch_tracks_async`
    fetchTracksAsync = fetch_tracks_async
