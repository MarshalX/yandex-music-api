from typing import TYPE_CHECKING, Optional, List

from yandex_music import YandexMusicObject
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client, TrackId


@model
class TrackShortOld(YandexMusicObject):
    """Класс, представляющий сокращённую версию трека.

    Note:
        Данная версия менее богата полями и найдена позже первой, поэтому была принята как за старую версию.

        Другая версия сокращённого трека: :class:`yandex_music.TrackShort`.

    Attributes:
        track_id (:obj:`yandex_music.TrackId`): Уникальный идентификатор трека.
        timestamp (:obj:`str`): Дата TODO.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    track_id: Optional['TrackId']
    timestamp: str
    client: Optional['Client'] = None

    def __post_init__(self):
        self._id_attrs = (self.track_id,)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['TrackShortOld']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.TrackShortOld`: Сокращённая версия трека или :obj:`None`.
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
            :obj:`list` из :obj:`yandex_music.TrackShortOld`: Сокращённые версии треков.
        """
        if not data:
            return []

        tracks = list()
        for track in data:
            tracks.append(cls.de_json(track, client))

        return tracks
