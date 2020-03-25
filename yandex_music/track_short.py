from typing import TYPE_CHECKING, Optional, List, Union

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client, Track


class TrackShort(YandexMusicObject):
    """Класс, представляющий укороченную версию трека с неполными данными.

    Attributes:
        id (:obj:`str`): Уникальный идентификатор трека.
        timestamp (:obj:`str`): Дата TODO.
        album_id (:obj:`str`): Уникальный идентификатор альбома.
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.

    Args:
        id_ (:obj:`str`): Уникальный идентификатор трека.
        timestamp (:obj:`str`): Дата TODO.
        album_id (:obj:`str`, optional): Уникальный идентификатор альбома.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 id_: Union[str, int],
                 timestamp: str,
                 album_id: Optional[str] = None,
                 client: Optional['Client'] = None,
                 **kwargs):
        self.id = id_
        self.timestamp = timestamp

        self.album_id = album_id

        self._track = None

        self.client = client
        self._id_attrs = (self.id, self.album_id)

    @property
    def track(self) -> 'Track':
        """:obj:`yandex_music.Track`: Полная версия трека."""
        if self._track:
            return self._track

        self._track = self.client.tracks(self.track_id)[0]

        return self._track

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

        tracks = list()
        for track in data:
            tracks.append(cls.de_json(track, client))

        return tracks

    # camelCase псевдонимы

    #: Псевдоним для :attr:`track_id`
    trackId = track_id
