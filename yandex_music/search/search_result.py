from typing import TYPE_CHECKING, Optional, List, Union

from yandex_music import YandexMusicObject, Artist, Album, Track, Playlist, Video

if TYPE_CHECKING:
    from yandex_music import Client


de_json_result = {
    'track': Track.de_list,
    'artist': Artist.de_list,
    'album': Album.de_list,
    'playlist': Playlist.de_list,
    'video': Video.de_list,
}


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
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.

    Args:
        type_ (:obj:`str`):  Тип результата.
        total (:obj:`int`): Количество результатов.
        per_page (:obj:`int`): Максимальное количество результатов на странице.
        order (:obj:`int`): Позиция блока.
        results (:obj:`list` из :obj:`yandex_music.Track` | :obj:`yandex_music.Artist` | :obj:`yandex_music.Album` \
            | :obj:`yandex_music.Playlist` | :obj:`yandex_music.Video`): Результаты поиска.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 type_: str,
                 total: int,
                 per_page: int,
                 order: int,
                 results: List[Union[Track, Artist, Album, Playlist, Video]],
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        super().handle_unknown_kwargs(self, **kwargs)

        self.type = type_
        self.total = total
        self.per_page = per_page
        self.order = order
        self.results = results

        self.client = client
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
        data['type_'] = type_
        data['results'] = de_json_result.get(type_)(data.get('results'), client)

        return cls(client=client, **data)
