from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, Context, JSONType, TrackId


@model
class Queue(YandexMusicModel):
    """Класс, представляющий очередь треков.

    Attributes:
        context (:obj:`yandex_music.Context` | :obj:`None`): Объект по которому построена очередь.
        tracks (:obj:`list` из :obj:`yandex_music.TrackId`): Список треков.
        current_index (:obj:`int`): Текущий проигрываемый трек.
        modified (:obj:`str`): Дата последнего изменения.
        id (:obj:`str`, optional): Уникальный идентификатор очереди.
        from_ (:obj:`str`, optional): Откуда был получен этот объект.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    context: Optional['Context']
    tracks: List['TrackId']
    current_index: int
    modified: str
    id: Optional[str] = None
    from_: Optional[str] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.id, self.tracks, self.context, self.modified)

    def get_current_track(self) -> 'TrackId':
        """Получение текущего трека очереди."""
        return self.tracks[self.current_index]

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['Queue']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Queue`: Очередь.
        """
        if not cls.is_dict_model_data(data):
            return None

        from yandex_music import Context, TrackId

        cls_data = cls.cleanup_data(data, client)
        cls_data['tracks'] = TrackId.de_list(data.get('tracks'), client)
        cls_data['context'] = Context.de_json(data.get('context'), client)

        return cls(client=client, **cls_data)  # type: ignore

    # camelCase псевдонимы

    #: Псевдоним для :attr:`get_current_track`
    getCurrentTrack = get_current_track
