from typing import List, TYPE_CHECKING, Optional

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client, TrackId, Context


class Queue(YandexMusicObject):
    """Класс, представляющий очередь треков.

    Attributes:
        context (:obj:`yandex_music.Context` | :obj:`None`): Объект по которому построена очередь.
        tracks (:obj:`list` из :obj:`yandex_music.TrackId`): Список треков.
        current_index (:obj:`int`): Текущий проигрываемый трек.
        modified (:obj:`str`): Дата последнего изменения.
        id (:obj:`str`): Уникальный идентификатор очереди.
        from_ (:obj:`str`): Откуда был получен этот объект.
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.

    Args:
        context (:obj:`yandex_music.Context` | :obj:`None`): Объект по которому построена очередь.
        tracks (:obj:`list` из :obj:`yandex_music.TrackId`): Список треков.
        current_index (:obj:`int`): Текущий проигрываемый трек.
        modified (:obj:`str`): Дата последнего изменения.
        id_ (:obj:`str`, optional): Уникальный идентификатор очереди.
        from_ (:obj:`str`, optional): Откуда был получен этот объект.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    def __init__(
        self,
        context: Optional['Context'],
        tracks: List['TrackId'],
        current_index: int,
        modified: str,
        id_: Optional[str] = None,
        from_: Optional[str] = None,
        client: Optional['Client'] = None,
        **kwargs,
    ):
        self.context = context
        self.tracks = tracks
        self.current_index = current_index
        self.modified = modified

        self.id = id_
        self.from_ = from_

        self.client = client
        self._id_attrs = (self.id, self.tracks, self.context, self.modified)

        super().handle_unknown_kwargs(self, **kwargs)

    def get_current_track(self) -> 'TrackId':
        """Получение текущего трека очереди."""
        return self.tracks[self.current_index]

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Queue']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Queue`: Очередь.
        """
        if not data:
            return None

        from yandex_music import TrackId, Context

        data = super(Queue, cls).de_json(data, client)
        data['tracks'] = TrackId.de_list(data.get('tracks'), client)
        data['context'] = Context.de_json(data.get('context'), client)

        return cls(client=client, **data)

    # camelCase псевдонимы

    #: Псевдоним для :attr:`get_current_track`
    getCurrentTrack = get_current_track
