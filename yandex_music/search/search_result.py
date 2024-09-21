from typing import TYPE_CHECKING, Dict, Generic, List, Optional, Type, TypeVar, Union

from yandex_music import Album, Artist, Playlist, Track, User, Video, YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType

T = TypeVar('T', bound=Union[Track, Artist, Album, Playlist, Video, User])


_TYPE_TO_CLASS: Dict[str, Type[YandexMusicModel]] = {
    'track': Track,
    'artist': Artist,
    'album': Album,
    'playlist': Playlist,
    'video': Video,
    'user': User,
    'podcast': Album,
    'podcast_episode': Track,
}


@model
class SearchResult(YandexMusicModel, Generic[T]):
    """Класс, представляющий результаты поиска.

    Note:
        Значения поля `type`: `track`, `artist`, `playlist`, `album`, `video`.

    Attributes:
        type (:obj:`str`): Тип результата.
        total (:obj:`int`): Количество результатов.
        per_page (:obj:`int`): Максимальное количество результатов на странице.
        order (:obj:`int`): Позиция блока.
        results (:obj:`list` из :obj:`yandex_music.Track` | :obj:`yandex_music.Artist` | :obj:`yandex_music.Album` \
            | :obj:`yandex_music.Playlist` | :obj:`yandex_music.Video`): Результаты поиска.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    type: str
    total: int
    per_page: int
    order: int
    results: List[T]
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.total, self.per_page, self.order, self.results)

    @classmethod
    def de_json(
        cls, data: 'JSONType', client: 'ClientType', type_: Optional[str] = None
    ) -> Optional['SearchResult[T]']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            type_ (:obj:`str`, optional): Тип результата.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.SearchResult`: Результаты поиска.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        cls_data['type'] = type_

        if type_ and type_ in _TYPE_TO_CLASS:
            klass = _TYPE_TO_CLASS[type_]
            cls_data['results'] = klass.de_list(data.get('results'), client)

        return cls(client=client, **cls_data)  # type: ignore
