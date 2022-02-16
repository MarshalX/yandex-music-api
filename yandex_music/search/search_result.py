from typing import TYPE_CHECKING, Optional, List, Union

from yandex_music import YandexMusicObject, Artist, Album, Track, Playlist, Video, User
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client


de_json_result = {
    'track': Track.de_list,
    'artist': Artist.de_list,
    'album': Album.de_list,
    'playlist': Playlist.de_list,
    'video': Video.de_list,
    'user': User.de_list,
    'podcast': Album.de_list,
    'podcast_episode': Track.de_list,
}


@model
class SearchResult(YandexMusicObject):
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
    results: List[Union[Track, Artist, Album, Playlist, Video]]
    client: Optional['Client'] = None

    def __post_init__(self):
        self._id_attrs = (self.total, self.per_page, self.order, self.results)

    @classmethod
    def de_json(cls, data: dict, client: 'Client', type_: str = None) -> Optional['SearchResult']:
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
        data['results'] = de_json_result.get(type_)(data.get('results'), client)

        return cls(client=client, **data)
