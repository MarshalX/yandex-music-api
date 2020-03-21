from typing import TYPE_CHECKING, Optional, List, Iterator

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client, TrackShort


class TracksList(YandexMusicObject):
    """Класс, представляющий список треков.

    Attributes:
        uid (:obj:`int`): Уникальный идентификатор пользователя.
        revision (:obj:`int`): Актуальность данных TODO.
        tracks (:obj:`list` из :obj:`yandex_music.TrackShort`): Список треков в укороченной версии.
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.

    Args:
        uid (:obj:`int`): Уникальный идентификатор пользователя.
        revision (:obj:`int`): Актуальность данных TODO.
        tracks (:obj:`list` из :obj:`yandex_music.TrackShort`): Список треков в укороченной версии.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 uid: int,
                 revision: int,
                 tracks: List['TrackShort'],
                 client: Optional['Client'] = None,
                 **kwargs):
        self.uid = uid
        self.revision = revision
        self.tracks = tracks

        self.client = client
        self._id_attrs = (self.uid, self.tracks)

    def __getitem__(self, item) -> 'TrackShort':
        return self.tracks[item]

    def __iter__(self) -> Iterator['TrackShort']:
        return iter(self.tracks)

    @property
    def tracks_ids(self) -> List[str]:
        """:obj:`list` из :obj:`str`: Список уникальных идентификаторов треков."""
        return [track.track_id for track in self.tracks]

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['TracksList']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.TracksList`: Список треков.
        """
        if not data:
            return None

        data = super(TracksList, cls).de_json(data, client)
        from yandex_music import TrackShort
        data['tracks'] = TrackShort.de_list(data.get('tracks'), client)

        return cls(client=client, **data)

    # camelCase псевдонимы

    #: Псевдоним для :attr:`tracks_ids`
    tracksIds = tracks_ids
