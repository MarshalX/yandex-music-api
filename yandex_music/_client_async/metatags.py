from typing import TYPE_CHECKING, Any, Optional

from yandex_music import (
    Metatag,
    MetatagAlbums,
    MetatagArtists,
    MetatagPlaylists,
    Metatags,
)
from yandex_music._client_async import log
from yandex_music._client_base import ClientBase

if TYPE_CHECKING:
    from yandex_music.utils.request_async import Request


class MetatagsMixin(ClientBase):
    """Метатеги.

    Миксин для методов, связанных с метатегами (подборки по настроениям, занятиям, жанрам и эпохам).
    """

    _request: 'Request'

    @log
    async def metatags(self, *args: Any, **kwargs: Any) -> Optional[Metatags]:
        """Получение дерева метатегов.

        Args:
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.Metatags` | :obj:`None`: Дерево метатегов или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/landing3/metatags'

        result = await self._request.get(url, *args, **kwargs)

        return Metatags.de_json(result, self)

    @log
    async def metatag(
        self,
        metatag_id: str,
        tracks_count: Optional[int] = None,
        artists_count: Optional[int] = None,
        composers_count: Optional[int] = None,
        albums_count: Optional[int] = None,
        promotions_count: Optional[int] = None,
        features_count: Optional[int] = None,
        playlists_count: Optional[int] = None,
        concerts_count: Optional[int] = None,
        tracks_sort_by: Optional[str] = None,
        albums_sort_by: Optional[str] = None,
        with_likes_count: Optional[bool] = None,
        *args: Any,
        **kwargs: Any,
    ) -> Optional[Metatag]:
        """Получение информации о метатеге.

        Note:
            Известные значения для `tracks_sort_by` и `albums_sort_by`: `popular`, `new`.

            Поля `tracks`, `composers`, `promotions`, `features` и `concerts` в модели
            :obj:`yandex_music.Metatag` не представлены, так как во всех опробованных
            метатегах возвращали пустой список.

        Args:
            metatag_id (:obj:`str`): Идентификатор метатега.
            tracks_count (:obj:`int`, optional): Количество треков в ответе.
            artists_count (:obj:`int`, optional): Количество артистов в ответе.
            composers_count (:obj:`int`, optional): Количество композиторов в ответе.
            albums_count (:obj:`int`, optional): Количество альбомов в ответе.
            promotions_count (:obj:`int`, optional): Количество промоакций в ответе.
            features_count (:obj:`int`, optional): Количество фич в ответе.
            playlists_count (:obj:`int`, optional): Количество плейлистов в ответе.
            concerts_count (:obj:`int`, optional): Количество концертов в ответе.
            tracks_sort_by (:obj:`str`, optional): Параметр сортировки треков.
            albums_sort_by (:obj:`str`, optional): Параметр сортировки альбомов.
            with_likes_count (:obj:`bool`, optional): Возвращать ли количество лайков.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.Metatag` | :obj:`None`: Метатег или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/metatags/{metatag_id}'

        raw_params = {
            'tracksCount': tracks_count,
            'artistsCount': artists_count,
            'composersCount': composers_count,
            'albumsCount': albums_count,
            'promotionsCount': promotions_count,
            'featuresCount': features_count,
            'playlistsCount': playlists_count,
            'concertsCount': concerts_count,
            'tracksSortBy': tracks_sort_by,
            'albumsSortBy': albums_sort_by,
            'withLikesCount': with_likes_count,
        }
        params = {k: v for k, v in raw_params.items() if v is not None}

        result = await self._request.get(url, params, *args, **kwargs)

        return Metatag.de_json(result, self)

    @log
    async def metatag_albums(
        self,
        metatag_id: str,
        period: Optional[str] = None,
        sort_by: Optional[str] = None,
        offset: int = 0,
        limit: int = 25,
        *args: Any,
        **kwargs: Any,
    ) -> Optional[MetatagAlbums]:
        """Получение альбомов метатега.

        Note:
            Известные значения для `sort_by`: `popular`, `new`.

        Args:
            metatag_id (:obj:`str`): Идентификатор метатега.
            period (:obj:`str`, optional): Период выборки.
            sort_by (:obj:`str`, optional): Параметр сортировки.
            offset (:obj:`int`, optional): Смещение от начала списка.
            limit (:obj:`int`, optional): Количество альбомов на странице.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.MetatagAlbums` | :obj:`None`: Страница списка альбомов метатега или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/metatags/{metatag_id}/albums'

        params: dict = {'offset': offset, 'limit': limit}
        if period is not None:
            params['period'] = period
        if sort_by is not None:
            params['sortBy'] = sort_by

        result = await self._request.get(url, params, *args, **kwargs)

        return MetatagAlbums.de_json(result, self)

    @log
    async def metatag_artists(
        self,
        metatag_id: str,
        period: str = 'week',
        sort_by: Optional[str] = None,
        offset: int = 0,
        limit: int = 25,
        tracks_per_artist: Optional[int] = None,
        *args: Any,
        **kwargs: Any,
    ) -> Optional[MetatagArtists]:
        """Получение артистов метатега.

        Note:
            Параметр `period` обязателен (без него API возвращает ошибку валидации).
            Известные значения для `period`: `week`, `month`, `day`.
            Известные значения для `sort_by`: `popular`.

        Args:
            metatag_id (:obj:`str`): Идентификатор метатега.
            period (:obj:`str`, optional): Период выборки.
            sort_by (:obj:`str`, optional): Параметр сортировки.
            offset (:obj:`int`, optional): Смещение от начала списка.
            limit (:obj:`int`, optional): Количество артистов на странице.
            tracks_per_artist (:obj:`int`, optional): Количество популярных треков на артиста.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.MetatagArtists` | :obj:`None`: Страница списка артистов метатега или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/metatags/{metatag_id}/artists'

        params: dict = {'period': period, 'offset': offset, 'limit': limit}
        if sort_by is not None:
            params['sortBy'] = sort_by
        if tracks_per_artist is not None:
            params['tracksPerArtist'] = tracks_per_artist

        result = await self._request.get(url, params, *args, **kwargs)

        return MetatagArtists.de_json(result, self)

    @log
    async def metatag_playlists(
        self,
        metatag_id: str,
        sort_by: Optional[str] = None,
        offset: int = 0,
        limit: int = 25,
        with_likes_count: Optional[bool] = None,
        *args: Any,
        **kwargs: Any,
    ) -> Optional[MetatagPlaylists]:
        """Получение плейлистов метатега.

        Note:
            Известные значения для `sort_by`: `popular`, `new`.

        Args:
            metatag_id (:obj:`str`): Идентификатор метатега.
            sort_by (:obj:`str`, optional): Параметр сортировки.
            offset (:obj:`int`, optional): Смещение от начала списка.
            limit (:obj:`int`, optional): Количество плейлистов на странице.
            with_likes_count (:obj:`bool`, optional): Возвращать ли количество лайков.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.MetatagPlaylists` | :obj:`None`: Страница списка плейлистов метатега или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/metatags/{metatag_id}/playlists'

        params: dict = {'offset': offset, 'limit': limit}
        if sort_by is not None:
            params['sortBy'] = sort_by
        if with_likes_count is not None:
            params['withLikesCount'] = with_likes_count

        result = await self._request.get(url, params, *args, **kwargs)

        return MetatagPlaylists.de_json(result, self)

    # camelCase псевдонимы

    #: Псевдоним для :attr:`metatag_albums`
    metatagAlbums = metatag_albums
    #: Псевдоним для :attr:`metatag_artists`
    metatagArtists = metatag_artists
    #: Псевдоним для :attr:`metatag_playlists`
    metatagPlaylists = metatag_playlists
