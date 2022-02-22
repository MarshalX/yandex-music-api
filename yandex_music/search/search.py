from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicObject
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client, Best, SearchResult


@model
class Search(YandexMusicObject):
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
    albums: Optional['SearchResult']
    artists: Optional['SearchResult']
    playlists: Optional['SearchResult']
    tracks: Optional['SearchResult']
    videos: Optional['SearchResult']
    users: Optional['SearchResult']
    podcasts: Optional['SearchResult']
    podcast_episodes: Optional['SearchResult']
    type: Optional[str] = None
    page: Optional[int] = None
    per_page: Optional[int] = None
    misspell_result: Optional[str] = None
    misspell_original: Optional[str] = None
    misspell_corrected: Optional[bool] = None
    nocorrect: Optional[bool] = None
    client: Optional['Client'] = None

    def __post_init__(self):
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

    def get_page(self, page: int, *args, **kwargs) -> Optional['Search']:
        """Получение определённой страницы поиска.

        Args:
            page (:obj:`int`): Номер страницы.

        Returns:
            :obj:`yandex_music.Search` | :obj:`None`: Страница результата поиска или :obj:`None`.
        """
        return self.client.search(self.text, self.nocorrect, self.type_, page, *args, **kwargs)

    async def get_page_async(self, page: int, *args, **kwargs) -> Optional['Search']:
        """Получение определённой страницы поиска.

        Args:
            page (:obj:`int`): Номер страницы.

        Returns:
            :obj:`yandex_music.Search` | :obj:`None`: Страница результата поиска или :obj:`None`.
        """
        return await self.client.search(self.text, self.nocorrect, self.type_, page, *args, **kwargs)

    def next_page(self, *args, **kwargs) -> Optional['Search']:
        """Получение следующей страницы поиска.

        Returns:
            :obj:`yandex_music.Search` | :obj:`None`: Следующая страница результата поиска или :obj:`None`.
        """
        return self.get_page(self.page + 1, *args, **kwargs)

    async def next_page_async(self, *args, **kwargs) -> Optional['Search']:
        """Получение следующей страницы поиска.

        Returns:
            :obj:`yandex_music.Search` | :obj:`None`: Следующая страница результата поиска или :obj:`None`.
        """
        return await self.get_page_async(self.page + 1, *args, **kwargs)

    def prev_page(self, *args, **kwargs) -> Optional['Search']:
        """Получение предыдущей страницы поиска.

        Returns:
            :obj:`yandex_music.Search` | :obj:`None`: Предыдущая страница результата поиска или :obj:`None`.
        """
        return self.get_page(self.page - 1, *args, **kwargs)

    async def prev_page_async(self, *args, **kwargs) -> Optional['Search']:
        """Получение предыдущей страницы поиска.

        Returns:
            :obj:`yandex_music.Search` | :obj:`None`: Предыдущая страница результата поиска или :obj:`None`.
        """
        return await self.get_page_async(self.page - 1, *args, **kwargs)

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

        # в ОЧЕНЬ редких случаях сервер творит дичь и может вернуть результат плейлистов в поле artists
        # или вернуть в поле users результаты с плейлистами

        # очень редких это около 10 запросов за 3 месяца работы стороннего клиента

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

    #: Псевдоним для :attr:`get_page`
    getPage = get_page
    #: Псевдоним для :attr:`get_page_async`
    getPageAsync = get_page_async
    #: Псевдоним для :attr:`next_page`
    nextPage = next_page
    #: Псевдоним для :attr:`next_page_async`
    nextPageASync = next_page_async
    #: Псевдоним для :attr:`prev_page`
    prevPage = prev_page
    #: Псевдоним для :attr:`prev_page_async`
    prevPageAsync = prev_page_async
