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
        users (:obj:`yandex_music.SearchResult`): Найденные пользователи.
        podcasts (:obj:`yandex_music.SearchResult`): Найденные подскасты.
        podcast_episodes (:obj:`yandex_music.SearchResult`): Найденные выпуски подкастов.
        type_ (:obj:`str`): Тип результата по которому искали (аргумент в Client.search).
        page (:obj:`int`): Текущая страница.
        per_page (:obj:`int`): Результатов на странице.
        misspell_result (:obj:`str`): Запрос с автоматическим исправлением.
        misspell_original (:obj:`str`): Оригинальный запрос.
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
        users (:obj:`yandex_music.SearchResult`): Найденные пользователи.
        podcasts (:obj:`yandex_music.SearchResult`): Найденные подскасты.
        podcast_episodes (:obj:`yandex_music.SearchResult`): Найденные выпуски подкастов.
        type_ (:obj:`str`), optional: Тип результата по которому искали (аргумент в Client.search).
        page (:obj:`int`, optional): Текущая страница.
        per_page (:obj:`int`, optional): Результатов на странице.
        misspell_result (:obj:`str`, optional): Запрос с автоматическим исправлением.
        misspell_original (:obj:`str`, optional): Оригинальный запрос.
        misspell_corrected (:obj:`bool`, optional): Был ли исправлен запрос.
        nocorrect (:obj:`bool`, optional): Было ли отключено исправление результата.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(
        self,
        search_request_id: str,
        text: str,
        best: Optional['Best'],
        albums: Optional['SearchResult'],
        artists: Optional['SearchResult'],
        playlists: Optional['SearchResult'],
        tracks: Optional['SearchResult'],
        videos: Optional['SearchResult'],
        users: Optional['SearchResult'],
        podcasts: Optional['SearchResult'],
        podcast_episodes: Optional['SearchResult'],
        type_: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
        misspell_result: Optional[str] = None,
        misspell_original: Optional[str] = None,
        misspell_corrected: Optional[bool] = None,
        nocorrect: Optional[bool] = None,
        client: Optional['Client'] = None,
        **kwargs,
    ) -> None:
        self.search_request_id = search_request_id
        self.text = text
        self.best = best
        self.albums = albums
        self.artists = artists
        self.playlists = playlists
        self.tracks = tracks
        self.videos = videos
        self.users = users

        self.podcasts = podcasts
        self.podcast_episodes = podcast_episodes
        self.type_ = type_
        self.page = page
        self.per_page = per_page
        self.misspell_result = misspell_result
        self.misspell_original = misspell_original
        self.misspell_corrected = misspell_corrected
        self.nocorrect = nocorrect

        self.client = client
        self._id_attrs = (
            self.search_request_id,
            self.text,
            self.best,
            self.albums,
            self.artists,
            self.playlists,
            self.tracks,
            self.videos,
            self.users,
            self.podcasts,
            self.podcast_episodes,
        )

        super().handle_unknown_kwargs(self, **kwargs)

    def get_page(self, page: int, *args, **kwargs) -> Optional['Search']:
        """Получение определеной страницы поиска.

        Args:
            page (:obj:`int`): Номер страницы.

        Returns:
            :obj:`yandex_music.Search` | :obj:`None`: Страница результата поиска или :obj:`None`.
        """
        return self.client.search(self.text, self.nocorrect, self.type_, page, *args, **kwargs)

    def next_page(self, *args, **kwargs) -> Optional['Search']:
        """Получение следующей страницы поиска.

        Returns:
            :obj:`yandex_music.Search` | :obj:`None`: Следующая страница результата поиска или :obj:`None`.
        """
        return self.get_page(self.page + 1, *args, **kwargs)

    def prev_page(self, *args, **kwargs) -> Optional['Search']:
        """Получение предыдущей страницы поиска.

        Returns:
            :obj:`yandex_music.Search` | :obj:`None`: Предыдущая страница результата поиска или :obj:`None`.
        """
        return self.get_page(self.page - 1, *args, **kwargs)

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
        data['users'] = SearchResult.de_json(data.get('users'), client, 'user')
        data['podcasts'] = SearchResult.de_json(data.get('podcasts'), client, 'podcast')
        data['podcast_episodes'] = SearchResult.de_json(data.get('podcast_episodes'), client, 'podcast_episode')

        return cls(client=client, **data)

    # camelCase псевдонимы

    #: Псевдоним для :attr:`next_page`
    nextPage = next_page
    #: Псевдоним для :attr:`prev_page`
    prevPage = prev_page
    #: Псевдоним для :attr:`get_page`
    getPage = get_page
