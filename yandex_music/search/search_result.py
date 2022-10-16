from typing import TYPE_CHECKING, Optional, List, Union, TypeVar, Generic, Type, Dict

from yandex_music import YandexMusicObject, Artist, Album, Track, Playlist, Video, User
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client

T = TypeVar('T', bound=Union[Track, Artist, Album, Playlist, Video])


type_class_by_str: Dict[str, Type[T]] = {
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
class SearchResult(YandexMusicObject, Generic[T]):
    """Класс, представляющий результаты поиска.

    Note:
        Значения поля `type`: `track`, `artist`, `playlist`, `album`, `video`.

    Attributes:
        type (:obj:`str`):  Тип результата.
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
    client: Optional['Client'] = None

    def __post_init__(self):
        self._id_attrs = (self.total, self.per_page, self.order, self.results)

    @classmethod
    def de_json(cls, data: Dict[str, Dict], client: 'Client', type_: str = None) -> Optional['SearchResult']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            type_ (:obj:`str`, optional): Тип результата.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.SearchResult`: Результаты поиска.
        """
        if not data:
            return None

        data = super(SearchResult, cls).de_json(data, client)
        data['type'] = type_
        type_class = type_class_by_str.get(type_)
        data['results'] = type_class.de_list(data.get('results'), client)

        return cls(client=client, **data)
