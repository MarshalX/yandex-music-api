from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client, Best, SearchResult


class Search(YandexMusicObject):
    """Класс, представляющий результаты поиска.

    Attributes:
        search_request_id (:obj:`str`): ID запроса.
        text (:obj:`str`): Текст запроса.
        best (:obj:`yandex_music.Best`): Лучший результат.
        albums (:obj:`yandex_music.SearchResult`): Найденные альбомы.
        artists (:obj:`yandex_music.SearchResult`): Найденные исполнители.
        playlists (:obj:`yandex_music.SearchResult`): Найденные плейлисты.
        tracks (:obj:`yandex_music.SearchResult`): Найденные треки.
        videos (:obj:`yandex_music.SearchResult`): Найденные видео.
        misspell_corrected (:obj:`bool`): Был ли исправлен запрос.
        nocorrect (:obj:`bool`): Было ли отключено исправление результата.
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.

    Args:
        search_request_id (:obj:`str`): ID запроса.
        text (:obj:`str`): Текст запроса.
        best (:obj:`yandex_music.Best`): Лучший результат.
        albums (:obj:`yandex_music.SearchResult`): Найденные альбомы.
        artists (:obj:`yandex_music.SearchResult`): Найденные исполнители.
        playlists (:obj:`yandex_music.SearchResult`): Найденные плейлисты.
        tracks (:obj:`yandex_music.SearchResult`): Найденные треки.
        videos (:obj:`yandex_music.SearchResult`): Найденные видео.
        misspell_corrected (:obj:`bool`, optional): Был ли исправлен запрос.
        nocorrect (:obj:`bool`, optional): Было ли отключено исправление результата.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 search_request_id: str,
                 text: str,
                 best: Optional['Best'],
                 albums: Optional['SearchResult'],
                 artists: Optional['SearchResult'],
                 playlists: Optional['SearchResult'],
                 tracks: Optional['SearchResult'],
                 videos: Optional['SearchResult'],
                 misspell_corrected: Optional[bool] = None,
                 nocorrect: Optional[bool] = None,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        super().handle_unknown_kwargs(self, **kwargs)

        self.search_request_id = search_request_id
        self.text = text
        self.best = best
        self.albums = albums
        self.artists = artists
        self.playlists = playlists
        self.tracks = tracks
        self.videos = videos

        self.misspell_corrected = misspell_corrected
        self.nocorrect = nocorrect

        self.client = client
        self._id_attrs = (self.search_request_id, self.text, self.best, self.albums,
                          self.artists, self.playlists, self.tracks, self.videos)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Search']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Search`: Результаты поиска.
        """
        if not data:
            return None

        data = super(Search, cls).de_json(data, client)
        from yandex_music import SearchResult, Best
        data['best'] = Best.de_json(data.get('best'), client)
        data['albums'] = SearchResult.de_json(data.get('albums'), client, 'album')
        data['artists'] = SearchResult.de_json(data.get('artists'), client, 'artist')
        data['playlists'] = SearchResult.de_json(data.get('playlists'), client, 'playlist')
        data['tracks'] = SearchResult.de_json(data.get('tracks'), client, 'track')
        data['videos'] = SearchResult.de_json(data.get('videos'), client, 'video')

        return cls(client=client, **data)
