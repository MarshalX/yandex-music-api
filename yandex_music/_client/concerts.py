#################################################################################################
# THIS IS AUTO GENERATED COPY OF yandex_music/_client_async/concerts.py. DON'T EDIT IT BY HANDS #
#################################################################################################

from typing import TYPE_CHECKING, Any, List, Optional, Union

from yandex_music import (
    ArtistConcerts,
    ConcertFeed,
    ConcertInfo,
    ConcertLocations,
    ConcertSkeleton,
    ConcertTabConfig,
)
from yandex_music._client import log
from yandex_music._client_base import ClientBase

if TYPE_CHECKING:
    from yandex_music.utils.request import Request


class ConcertsMixin(ClientBase):
    """Концерты.

    Миксин для методов, связанных с концертами и афишей.
    """

    _request: 'Request'

    @log
    def artists_concerts(
        self,
        artist_id: Union[str, int],
        *args: Any,
        **kwargs: Any,
    ) -> Optional[ArtistConcerts]:
        """Получение концертов артиста.

        Args:
            artist_id (:obj:`str` | :obj:`int`): Уникальный идентификатор артиста.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.ArtistConcerts` | :obj:`None`: Информация о концертах артиста или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/artists/{artist_id}/concerts'

        result = self._request.get(url, *args, **kwargs)

        return ArtistConcerts.de_json(result, self)

    @log
    def concert_info(self, concert_id: str, *args: Any, **kwargs: Any) -> Optional[ConcertInfo]:
        """Получение информации о концерте.

        Args:
            concert_id (:obj:`str`): Уникальный идентификатор концерта (UUID).
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.ConcertInfo` | :obj:`None`: Информация о концерте или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/concerts/{concert_id}/info'

        result = self._request.get(url, *args, **kwargs)

        return ConcertInfo.de_json(result, self)

    @log
    def concert_skeleton(
        self,
        concert_id: str,
        skeleton_id: str = 'concert_page',
        *args: Any,
        **kwargs: Any,
    ) -> Optional[ConcertSkeleton]:
        """Получение скелетона страницы концерта.

        Args:
            concert_id (:obj:`str`): Уникальный идентификатор концерта (UUID).
            skeleton_id (:obj:`str`, optional): Идентификатор скелетона.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.ConcertSkeleton` | :obj:`None`: Скелетон страницы концерта или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/concerts/{concert_id}/skeletons/{skeleton_id}'

        result = self._request.get(url, *args, **kwargs)

        return ConcertSkeleton.de_json(result, self)

    @log
    def concerts_feed(
        self,
        locations: Optional[List[Union[str, int]]] = None,
        *args: Any,
        **kwargs: Any,
    ) -> Optional[ConcertFeed]:
        """Получение ленты концертов.

        Args:
            locations (:obj:`list` из :obj:`str` | :obj:`int`, optional): Список идентификаторов
                местоположений (geoId) для фильтрации ленты.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.ConcertFeed` | :obj:`None`: Лента концертов или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/concerts/feed'

        params = {}
        if locations:
            params['locations'] = ','.join(str(location) for location in locations)

        result = self._request.get(url, params, *args, **kwargs)

        return ConcertFeed.de_json(result, self)

    @log
    def concerts_locations(self, *args: Any, **kwargs: Any) -> Optional[ConcertLocations]:
        """Получение списка местоположений для фильтрации концертов.

        Args:
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.ConcertLocations` | :obj:`None`: Список местоположений или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/concerts/locations'

        result = self._request.get(url, *args, **kwargs)

        return ConcertLocations.de_json(result, self)

    @log
    def concerts_tab_config(self, *args: Any, **kwargs: Any) -> Optional[ConcertTabConfig]:
        """Получение конфигурации вкладок концертов.

        Args:
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.ConcertTabConfig` | :obj:`None`: Конфигурация вкладок или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/concerts/tab-config'

        result = self._request.get(url, *args, **kwargs)

        return ConcertTabConfig.de_json(result, self)

    # camelCase псевдонимы

    #: Псевдоним для :attr:`artists_concerts`
    artistsConcerts = artists_concerts
    #: Псевдоним для :attr:`concert_info`
    concertInfo = concert_info
    #: Псевдоним для :attr:`concert_skeleton`
    concertSkeleton = concert_skeleton
    #: Псевдоним для :attr:`concerts_feed`
    concertsFeed = concerts_feed
    #: Псевдоним для :attr:`concerts_locations`
    concertsLocations = concerts_locations
    #: Псевдоним для :attr:`concerts_tab_config`
    concertsTabConfig = concerts_tab_config
