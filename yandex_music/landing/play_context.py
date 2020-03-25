from typing import TYPE_CHECKING, Optional, List

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client, TrackShortOld


class PlayContext(YandexMusicObject):
    """Класс, представляющий проигрываемый контекст.

    Note:
        Известные значения поля `client_`: `android`.

        Поле `context` хранит в себе место воспроизведения, например, `playlist`.

        Поле `context_item` хранит в себе уникальный идентификатор context'a, т.е. в нашем случае playlist'a.

    Attributes:
        client_ (:obj:`str`): Клиент.
        context (:obj:`str`): Тип контекста.
        context_item (:obj:`str`): Предмет контекста.
        tracks (:obj:`list` из :obj:`yandex_music.TrackShortOld`): Треки.
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.

    Args:
        client_ (:obj:`str`): Клиент.
        context (:obj:`str`): Тип контекста.
        context_item (:obj:`str`): Предмет контекста.
        tracks (:obj:`list` из :obj:`yandex_music.TrackShortOld`): Треки.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 client_: str,
                 context: str,
                 context_item: str,
                 tracks: List['TrackShortOld'],
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        super().handle_unknown_kwargs(self, **kwargs)

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
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.PlayContext`: Проигрываемый контекст.
        """
        if not data:
            return None

        data = super(PlayContext, cls).de_json(data, client)
        from yandex_music import TrackShortOld
        data['tracks'] = TrackShortOld.de_list(data.get('tracks'), client)

        return cls(client=client, **data)
