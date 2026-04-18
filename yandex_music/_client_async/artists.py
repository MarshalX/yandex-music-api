from typing import TYPE_CHECKING, Any, List, Optional, Union

from yandex_music import (
    Artist,
    ArtistAbout,
    ArtistAlbums,
    ArtistClips,
    ArtistDonations,
    ArtistInfo,
    ArtistLinks,
    ArtistSimilar,
    ArtistSkeleton,
    ArtistTracks,
    ArtistTrailer,
    BriefInfo,
)
from yandex_music._client_async import log
from yandex_music._client_async._batch import _BatchMixin

if TYPE_CHECKING:
    from yandex_music.utils.request_async import Request


class ArtistsMixin(_BatchMixin):
    """Артисты.

    Миксин для методов, связанных с артистами.
    """

    _request: 'Request'

    @log
    async def artists(
        self, artist_ids: Union[List[Union[str, int]], int, str], *args: Any, **kwargs: Any
    ) -> List[Artist]:
        """Получение исполнителя/исполнителей.

        Args:
            artist_ids (:obj:`str` | :obj:`int` | :obj:`list` из :obj:`str` | :obj:`list` из :obj:`int`): Уникальный
                идентификатор исполнителя или исполнителей.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`list` из :obj:`yandex_music.Artist`: Исполнитель или исполнители.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        return await self._get_list('artist', artist_ids, *args, **kwargs)

    @log
    async def artists_brief_info(self, artist_id: Union[str, int], *args: Any, **kwargs: Any) -> Optional[BriefInfo]:
        """Получение информации об артисте.

        Args:
            artist_id (:obj:`str` | :obj:`int`): Уникальный идентификатор исполнителя.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.BriefInfo` | :obj:`None`: Информация об артисте или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/artists/{artist_id}/brief-info'

        result = await self._request.get(url, *args, **kwargs)

        return BriefInfo.de_json(result, self)

    @log
    async def artists_tracks(
        self,
        artist_id: Union[str, int],
        page: int = 0,
        page_size: int = 20,
        *args: Any,
        **kwargs: Any,
    ) -> Optional[ArtistTracks]:
        """Получение треков артиста.

        Args:
            artist_id (:obj:`str` | :obj:`int`): Уникальный идентификатор артиста.
            page (:obj:`int`, optional): Номер страницы.
            page_size (:obj:`int`, optional): Количество треков на странице.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.ArtistsTracks` | :obj:`None`: Страница списка треков артиста или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/artists/{artist_id}/tracks'

        params = {'page': page, 'page-size': page_size}

        result = await self._request.get(url, params, *args, **kwargs)

        return ArtistTracks.de_json(result, self)

    @log
    async def artists_direct_albums(
        self,
        artist_id: Union[str, int],
        page: int = 0,
        page_size: int = 20,
        sort_by: str = 'year',
        *args: Any,
        **kwargs: Any,
    ) -> Optional[ArtistAlbums]:
        """Получение альбомов артиста.

        Note:
            Известные значения для `sort_by`: `year`, `rating`.

        Args:
            artist_id (:obj:`str` | :obj:`int`): Уникальный идентификатор артиста.
            page (:obj:`int`, optional): Номер страницы.
            page_size (:obj:`int`, optional): Количество альбомов на странице.
            sort_by (:obj:`str`, optional): Параметр для сортировки.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.ArtistAlbums` | :obj:`None`: Страница списка альбомов артиста или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/artists/{artist_id}/direct-albums'

        params = {'sort-by': sort_by, 'page': page, 'page-size': page_size}

        result = await self._request.get(url, params, *args, **kwargs)

        return ArtistAlbums.de_json(result, self)

    @log
    async def artists_similar(
        self,
        artist_id: Union[str, int],
        *args: Any,
        **kwargs: Any,
    ) -> Optional[ArtistSimilar]:
        """Получение похожих артистов.

        Args:
            artist_id (:obj:`str` | :obj:`int`): Уникальный идентификатор артиста.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.ArtistSimilar` | :obj:`None`: Похожие артисты или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/artists/{artist_id}/similar'

        result = await self._request.get(url, *args, **kwargs)

        return ArtistSimilar.de_json(result, self)

    @log
    async def artists_links(
        self,
        artist_id: Union[str, int],
        *args: Any,
        **kwargs: Any,
    ) -> Optional[ArtistLinks]:
        """Получение ссылок на страницы артиста.

        Args:
            artist_id (:obj:`str` | :obj:`int`): Уникальный идентификатор артиста.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.ArtistLinks` | :obj:`None`: Ссылки на страницы артиста или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/artists/{artist_id}/artist-links'

        result = await self._request.get(url, *args, **kwargs)

        return ArtistLinks.de_json(result, self)

    @log
    async def artists_also_albums(
        self,
        artist_id: Union[str, int],
        page: int = 0,
        page_size: int = 20,
        sort_by: str = 'year',
        *args: Any,
        **kwargs: Any,
    ) -> Optional[ArtistAlbums]:
        """Получение сборников и альбомов, в которых участвовал артист.

        Note:
            Известные значения для `sort_by`: `year`, `rating`.

        Args:
            artist_id (:obj:`str` | :obj:`int`): Уникальный идентификатор артиста.
            page (:obj:`int`, optional): Номер страницы.
            page_size (:obj:`int`, optional): Количество альбомов на странице.
            sort_by (:obj:`str`, optional): Параметр для сортировки.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.ArtistAlbums` | :obj:`None`: Страница списка альбомов артиста или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/artists/{artist_id}/also-albums'

        params = {'sort-by': sort_by, 'page': page, 'page-size': page_size}

        result = await self._request.get(url, params, *args, **kwargs)

        return ArtistAlbums.de_json(result, self)

    @log
    async def artists_discography_albums(
        self,
        artist_id: Union[str, int],
        page: int = 0,
        page_size: int = 20,
        sort_by: str = 'year',
        *args: Any,
        **kwargs: Any,
    ) -> Optional[ArtistAlbums]:
        """Получение дискографии артиста.

        Note:
            Известные значения для `sort_by`: `year`, `rating`.

        Args:
            artist_id (:obj:`str` | :obj:`int`): Уникальный идентификатор артиста.
            page (:obj:`int`, optional): Номер страницы.
            page_size (:obj:`int`, optional): Количество альбомов на странице.
            sort_by (:obj:`str`, optional): Параметр для сортировки.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.ArtistAlbums` | :obj:`None`: Страница списка дискографии артиста или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/artists/{artist_id}/discography-albums'

        params = {'sort-by': sort_by, 'page': page, 'page-size': page_size}

        result = await self._request.get(url, params, *args, **kwargs)

        return ArtistAlbums.de_json(result, self)

    @log
    async def artists_safe_direct_albums(
        self,
        artist_id: Union[str, int],
        sort_by: str = 'year',
        sort_order: str = 'desc',
        limit: int = 20,
        *args: Any,
        **kwargs: Any,
    ) -> Optional[ArtistAlbums]:
        """Получение безопасных альбомов артиста.

        Note:
            Известные значения для `sort_by`: `year`, `rating`.
            Известные значения для `sort_order`: `asc`, `desc`.

        Args:
            artist_id (:obj:`str` | :obj:`int`): Уникальный идентификатор артиста.
            sort_by (:obj:`str`, optional): Параметр для сортировки.
            sort_order (:obj:`str`, optional): Порядок сортировки.
            limit (:obj:`int`, optional): Количество альбомов.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.ArtistAlbums` | :obj:`None`: Список альбомов артиста или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/artists/{artist_id}/safe-direct-albums'

        params = {'sort-by': sort_by, 'sort-order': sort_order, 'limit': limit}

        result = await self._request.get(url, params, *args, **kwargs)

        return ArtistAlbums.de_json(result, self)

    @log
    async def artists_track_ids(
        self,
        artist_id: Union[str, int],
        page: int = 0,
        page_size: int = 20,
        *args: Any,
        **kwargs: Any,
    ) -> List[str]:
        """Получение идентификаторов треков артиста.

        Args:
            artist_id (:obj:`str` | :obj:`int`): Уникальный идентификатор артиста.
            page (:obj:`int`, optional): Номер страницы.
            page_size (:obj:`int`, optional): Количество треков на странице.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`list` из :obj:`str`: Список идентификаторов треков.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/artists/{artist_id}/track-ids'

        params = {'page': page, 'page-size': page_size}

        result = await self._request.get(url, params, *args, **kwargs)

        if isinstance(result, list):
            return result

        return []

    @log
    async def artists_about(
        self,
        artist_id: Union[str, int],
        *args: Any,
        **kwargs: Any,
    ) -> Optional[ArtistAbout]:
        """Получение информации «Об артисте».

        Args:
            artist_id (:obj:`str` | :obj:`int`): Уникальный идентификатор артиста.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.ArtistAbout` | :obj:`None`: Информация «Об артисте» или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/artists/{artist_id}/about-artist'

        result = await self._request.get(url, *args, **kwargs)

        return ArtistAbout.de_json(result, self)

    @log
    async def artists_clips(
        self,
        artist_id: Union[str, int],
        *args: Any,
        **kwargs: Any,
    ) -> Optional[ArtistClips]:
        """Получение клипов артиста.

        Args:
            artist_id (:obj:`str` | :obj:`int`): Уникальный идентификатор артиста.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.ArtistClips` | :obj:`None`: Клипы артиста или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/artists/{artist_id}/blocks/artist-clips'

        result = await self._request.get(url, *args, **kwargs)

        return ArtistClips.de_json(result, self)

    @log
    async def artists_donation(
        self,
        artist_id: Union[str, int],
        *args: Any,
        **kwargs: Any,
    ) -> Optional[ArtistDonations]:
        """Получение информации о донатах артиста.

        Args:
            artist_id (:obj:`str` | :obj:`int`): Уникальный идентификатор артиста.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.ArtistDonations` | :obj:`None`: Информация о донатах артиста или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/artists/{artist_id}/blocks/artist-donation'

        result = await self._request.get(url, *args, **kwargs)

        return ArtistDonations.de_json(result, self)

    @log
    async def artists_info(
        self,
        artist_id: Union[str, int],
        *args: Any,
        **kwargs: Any,
    ) -> Optional[ArtistInfo]:
        """Получение подробной информации об артисте.

        Args:
            artist_id (:obj:`str` | :obj:`int`): Уникальный идентификатор артиста.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.ArtistInfo` | :obj:`None`: Подробная информация об артисте или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/artists/{artist_id}/info'

        result = await self._request.get(url, *args, **kwargs)

        return ArtistInfo.de_json(result, self)

    @log
    async def artists_skeleton(
        self,
        artist_id: Union[str, int],
        skeleton_id: str = 'web-artist-default',
        *args: Any,
        **kwargs: Any,
    ) -> Optional[ArtistSkeleton]:
        """Получение скелетона страницы артиста.

        Args:
            artist_id (:obj:`str` | :obj:`int`): Уникальный идентификатор артиста.
            skeleton_id (:obj:`str`, optional): Идентификатор скелетона.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.ArtistSkeleton` | :obj:`None`: Скелетон страницы артиста или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/artists/{artist_id}/skeletons/{skeleton_id}'

        result = await self._request.get(url, *args, **kwargs)

        return ArtistSkeleton.de_json(result, self)

    @log
    async def artists_trailer(
        self,
        artist_id: Union[str, int],
        *args: Any,
        **kwargs: Any,
    ) -> Optional[ArtistTrailer]:
        """Получение трейлера артиста.

        Args:
            artist_id (:obj:`str` | :obj:`int`): Уникальный идентификатор артиста.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.ArtistTrailer` | :obj:`None`: Трейлер артиста или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/artists/{artist_id}/trailer'

        result = await self._request.get(url, *args, **kwargs)

        return ArtistTrailer.de_json(result, self)

    # camelCase псевдонимы

    #: Псевдоним для :attr:`artists_brief_info`
    artistsBriefInfo = artists_brief_info
    #: Псевдоним для :attr:`artists_tracks`
    artistsTracks = artists_tracks
    #: Псевдоним для :attr:`artists_direct_albums`
    artistsDirectAlbums = artists_direct_albums
    #: Псевдоним для :attr:`artists_similar`
    artistsSimilar = artists_similar
    #: Псевдоним для :attr:`artists_links`
    artistsLinks = artists_links
    #: Псевдоним для :attr:`artists_also_albums`
    artistsAlsoAlbums = artists_also_albums
    #: Псевдоним для :attr:`artists_discography_albums`
    artistsDiscographyAlbums = artists_discography_albums
    #: Псевдоним для :attr:`artists_safe_direct_albums`
    artistsSafeDirectAlbums = artists_safe_direct_albums
    #: Псевдоним для :attr:`artists_track_ids`
    artistsTrackIds = artists_track_ids
    #: Псевдоним для :attr:`artists_about`
    artistsAbout = artists_about
    #: Псевдоним для :attr:`artists_clips`
    artistsClips = artists_clips
    #: Псевдоним для :attr:`artists_donation`
    artistsDonation = artists_donation
    #: Псевдоним для :attr:`artists_info`
    artistsInfo = artists_info
    #: Псевдоним для :attr:`artists_skeleton`
    artistsSkeleton = artists_skeleton
    #: Псевдоним для :attr:`artists_trailer`
    artistsTrailer = artists_trailer
