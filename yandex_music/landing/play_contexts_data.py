from typing import TYPE_CHECKING, Optional, List

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client, TrackShortOld


class PlayContextsData(YandexMusicObject):
    """Класс, представляющий .

    Attributes:
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.

    Args:
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 other_tracks: List['TrackShortOld'],
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        self.other_tracks = other_tracks

        self.client = client
        self._id_attrs = (self.other_tracks,)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['PlayContextsData']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.PlayContextsData`: TODO.
        """
        if not data:
            return None

        data = super(PlayContextsData, cls).de_json(data, client)
        from yandex_music import TrackShortOld
        data['other_tracks'] = TrackShortOld.de_list(data.get('other_tracks'), client)

        return cls(client=client, **data)
