from datetime import datetime

from yandex_music import YandexMusicObject


class TrackShort(YandexMusicObject):
    """Класс представляющий укороченную версию трека с неполными данными.

    Attributes:
        id (:obj:`str`): Уникальный идентификатор трека.
        timestamp (:obj:`datetime.datetime`): Дата TODO.
        album_id (:obj:`str`): Уникальный идентификатор альбома.
        client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
            Music.

    Args:
        id (:obj:`str`): Уникальный идентификатор трека.
        timestamp (:obj:`str`): Дата TODO.
        album_id (:obj:`str`, optional): Уникальный идентификатор альбома.
        client (:obj:`yandex_music.Client`, optional): Объект класса :class:`yandex_music.Client` представляющий клиент
            Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 id,
                 timestamp,
                 album_id=None,
                 client=None,
                 **kwargs):
        self.id = id
        self.timestamp = datetime.fromisoformat(timestamp)

        self.album_id = album_id

        self._track = None

        self.client = client

    @property
    def track(self):
        """:obj:`yandex_music.Track`: Объект класса :class:`yandex_music.Track` представляющий полную версию трека."""
        if self._track:
            return self._track

        self._track = self.client.tracks(self.track_id)[0]

        return self._track

    @property
    def track_id(self):
        """:obj:`str`:  Уникальный идентификатор трека состоящий из его номера и номера альбома или просто из номера."""

        if self.album_id:
            return f'{self.id}:{self.album_id}'

        return f'{self.id}'

    @classmethod
    def de_json(cls, data, client):
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
                Music.

        Returns:
            :obj:`yandex_music.TrackShort`: Объект класса :class:`yandex_music.TrackShort`.
        """
        if not data:
            return None

        data = super(TrackShort, cls).de_json(data, client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data, client):
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
                Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.TrackShort`: Список объектов класса :class:`yandex_music.TrackShort`.
        """
        if not data:
            return []

        tracks = list()
        for track in data:
            tracks.append(cls.de_json(track, client))

        return tracks
