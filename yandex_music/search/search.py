from typing import TYPE_CHECKING, Any, Optional

from yandex_music import Album, Artist, JSONType, Playlist, Track, User, Video, YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Best, ClientType, SearchResult


@model
class Search(YandexMusicModel):
    """Класс, представляющий результаты поиска.

    Attributes:
        search_request_id (:obj:`str`): ID запроса.
        text (:obj:`str`): Текст запроса.
        best (:obj:`yandex_music.Best`, optional): Лучший результат.
        albums (:obj:`yandex_music.SearchResult`, optional): Найденные альбомы.
        artists (:obj:`yandex_music.SearchResult`, optional): Найденные исполнители.
        playlists (:obj:`yandex_music.SearchResult`, optional): Найденные плейлисты.
        tracks (:obj:`yandex_music.SearchResult`, optional): Найденные треки.
        videos (:obj:`yandex_music.SearchResult`, optional): Найденные видео.
        users (:obj:`yandex_music.SearchResult`, optional): Найденные пользователи.
        podcasts (:obj:`yandex_music.SearchResult`, optional): Найденные подкасты.
        podcast_episodes (:obj:`yandex_music.SearchResult`, optional): Найденные выпуски подкастов.
        type (:obj:`str`), optional: Тип результата по которому искали (аргумент в Client.search).
        page (:obj:`int`, optional): Текущая страница.
        per_page (:obj:`int`, optional): Результатов на странице.
        misspell_result (:obj:`str`, optional): Запрос с автоматическим исправлением.
        misspell_original (:obj:`str`, optional): Оригинальный запрос.
        misspell_corrected (:obj:`bool`, optional): Был ли исправлен запрос.
        nocorrect (:obj:`bool`, optional): Было ли отключено исправление результата.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    search_request_id: str
    text: str
    best: Optional['Best']
    albums: Optional['SearchResult[Album]']
    artists: Optional['SearchResult[Artist]']
    playlists: Optional['SearchResult[Playlist]']
    tracks: Optional['SearchResult[Track]']
    videos: Optional['SearchResult[Video]']
    users: Optional['SearchResult[User]']
    podcasts: Optional['SearchResult[Album]']
    podcast_episodes: Optional['SearchResult[Track]']
    type: Optional[str] = None
    page: Optional[int] = None
    per_page: Optional[int] = None
    misspell_result: Optional[str] = None
    misspell_original: Optional[str] = None
    misspell_corrected: Optional[bool] = None
    nocorrect: Optional[bool] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
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

    def get_page(self, page: int, *args: Any, **kwargs: Any) -> Optional['Search']:
        """Получение определённой страницы поиска.

        Args:
            page (:obj:`int`): Номер страницы.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.Search` | :obj:`None`: Страница результата поиска или :obj:`None`.
        """
        assert isinstance(self.nocorrect, bool)
        assert isinstance(self.type, str)
        assert self.valid_client(self.client)
        return self.client.search(self.text, self.nocorrect, self.type, page, *args, **kwargs)

    async def get_page_async(self, page: int, *args: Any, **kwargs: Any) -> Optional['Search']:
        """Получение определённой страницы поиска.

        Args:
            page (:obj:`int`): Номер страницы.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.Search` | :obj:`None`: Страница результата поиска или :obj:`None`.
        """
        assert isinstance(self.nocorrect, bool)
        assert isinstance(self.type, str)
        assert self.valid_async_client(self.client)
        return await self.client.search(self.text, self.nocorrect, self.type, page, *args, **kwargs)

    def next_page(self, *args: Any, **kwargs: Any) -> Optional['Search']:
        """Получение следующей страницы поиска.

        Returns:
            :obj:`yandex_music.Search` | :obj:`None`: Следующая страница результата поиска или :obj:`None`.
        """
        assert isinstance(self.page, int)
        return self.get_page(self.page + 1, *args, **kwargs)

    async def next_page_async(self, *args: Any, **kwargs: Any) -> Optional['Search']:
        """Получение следующей страницы поиска.

        Returns:
            :obj:`yandex_music.Search` | :obj:`None`: Следующая страница результата поиска или :obj:`None`.
        """
        assert isinstance(self.page, int)
        return await self.get_page_async(self.page + 1, *args, **kwargs)

    def prev_page(self, *args: Any, **kwargs: Any) -> Optional['Search']:
        """Получение предыдущей страницы поиска.

        Returns:
            :obj:`yandex_music.Search` | :obj:`None`: Предыдущая страница результата поиска или :obj:`None`.
        """
        assert isinstance(self.page, int)
        return self.get_page(self.page - 1, *args, **kwargs)

    async def prev_page_async(self, *args: Any, **kwargs: Any) -> Optional['Search']:
        """Получение предыдущей страницы поиска.

        Returns:
            :obj:`yandex_music.Search` | :obj:`None`: Предыдущая страница результата поиска или :obj:`None`.
        """
        assert isinstance(self.page, int)
        return await self.get_page_async(self.page - 1, *args, **kwargs)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['Search']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Search`: Результаты поиска.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music import Best, SearchResult

        # в ОЧЕНЬ редких случаях сервер творит дичь и может вернуть результат плейлистов в поле artists
        # или вернуть в поле users результаты с плейлистами

        # очень редких это около 10 запросов за 3 месяца работы стороннего клиента

        cls_data['best'] = Best.de_json(data.get('best'), client)
        cls_data['albums'] = SearchResult.de_json(data.get('albums'), client, 'album')
        cls_data['artists'] = SearchResult.de_json(data.get('artists'), client, 'artist')
        cls_data['playlists'] = SearchResult.de_json(data.get('playlists'), client, 'playlist')
        cls_data['tracks'] = SearchResult.de_json(data.get('tracks'), client, 'track')
        cls_data['videos'] = SearchResult.de_json(data.get('videos'), client, 'video')
        cls_data['users'] = SearchResult.de_json(data.get('users'), client, 'user')
        cls_data['podcasts'] = SearchResult.de_json(data.get('podcasts'), client, 'podcast')
        cls_data['podcast_episodes'] = SearchResult.de_json(data.get('podcast_episodes'), client, 'podcast_episode')

        return cls(client=client, **cls_data)  # type: ignore

    # camelCase псевдонимы

    #: Псевдоним для :attr:`get_page`
    getPage = get_page
    #: Псевдоним для :attr:`get_page_async`
    getPageAsync = get_page_async
    #: Псевдоним для :attr:`next_page`
    nextPage = next_page
    #: Псевдоним для :attr:`next_page_async`
    nextPageAsync = next_page_async
    #: Псевдоним для :attr:`prev_page`
    prevPage = prev_page
    #: Псевдоним для :attr:`prev_page_async`
    prevPageAsync = prev_page_async
