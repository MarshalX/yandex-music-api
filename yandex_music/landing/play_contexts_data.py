from typing import TYPE_CHECKING, Optional, List

from yandex_music import YandexMusicObject
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client, TrackShortOld


@model
class PlayContextsData(YandexMusicObject):
    """Класс, представляющий данные проигрываемого контекста.

    Attributes:
        other_tracks (:obj:`list` из :obj:`yandex_music.TrackShortOld`): Другие треки.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    other_tracks: List['TrackShortOld']
    client: Optional['Client'] = None

    def __post_init__(self):
        self._id_attrs = (self.other_tracks,)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['PlayContextsData']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.PlayContextsData`: Данные проигрываемого контекста.
        """
        if not data:
            return None

        data = super(PlayContextsData, cls).de_json(data, client)
        from yandex_music import TrackShortOld

        data['other_tracks'] = TrackShortOld.de_list(data.get('other_tracks'), client)

        return cls(client=client, **data)
