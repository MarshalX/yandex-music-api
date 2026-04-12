from typing import TYPE_CHECKING, Any, Optional, Union

from yandex_music import ArtistAlbums, ArtistTracks, BriefInfo
from yandex_music._client_async import log
from yandex_music._client_base import ClientBase

if TYPE_CHECKING:
    from yandex_music.utils.request_async import Request


class ArtistsMixin(ClientBase):
    """Миксин для методов, связанных с артистами."""

    _request: 'Request'

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

    # camelCase псевдонимы

    #: Псевдоним для :attr:`artists_brief_info`
    artistsBriefInfo = artists_brief_info
    #: Псевдоним для :attr:`artists_tracks`
    artistsTracks = artists_tracks
    #: Псевдоним для :attr:`artists_direct_albums`
    artistsDirectAlbums = artists_direct_albums
