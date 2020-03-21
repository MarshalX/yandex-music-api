from typing import TYPE_CHECKING, Optional, List

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client, TrackId


class TrackShortOld(YandexMusicObject):
    """Класс, представляющий .

    Attributes:
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

    Args:
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 track_id: Optional['TrackId'],
                 timestamp: str,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        self.track_id = track_id
        self.timestamp = timestamp

        self.client = client
        self._id_attrs = (self.track_id,)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['TrackShortOld']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.TrackShortOld`: TODO.
        """
        if not data:
            return None

        data = super(TrackShortOld, cls).de_json(data, client)
        from yandex_music import TrackId
        data['track_id'] = TrackId.de_json(data.get('track_id'), client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data: dict, client: 'Client') -> List['TrackShortOld']:
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.TrackShortOld`: TODO.
        """
        if not data:
            return []

        tracks = list()
        for track in data:
            tracks.append(cls.de_json(track, client))

        return tracks
