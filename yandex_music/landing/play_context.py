from typing import TYPE_CHECKING, Optional, List

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client, TrackShortOld


class PlayContext(YandexMusicObject):
    """Класс, представляющий .

    Attributes:
        client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

    Args:
        client (:obj:`yandex_music.Client`, optional): Объект класса :class:`yandex_music.Client`, представляющий клиент
            Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 client_: str,
                 context: str,
                 context_item: str,
                 tracks: List['TrackShortOld'],
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        self.client_ = client_
        self.context = context
        self.context_item = context_item
        self.tracks = tracks

        self.client = client
        self._id_attrs = (self.client_, self.context_item, self.context_item, self.tracks)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['PlayContext']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

        Returns:
            :obj:`yandex_music.PlayContext`: Объект класса :class:`yandex_music.PlayContext`.
        """
        if not data:
            return None

        data = super(PlayContext, cls).de_json(data, client)
        from yandex_music import TrackShortOld
        data['tracks'] = TrackShortOld.de_list(data.get('tracks'), client)

        return cls(client=client, **data)
