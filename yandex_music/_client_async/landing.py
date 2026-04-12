from typing import TYPE_CHECKING, Any, List, Optional, Union, cast

from yandex_music import ChartInfo, Feed, Genre, Landing, LandingList, TagResult
from yandex_music._client_async import log
from yandex_music._client_base import ClientBase

if TYPE_CHECKING:
    from yandex_music.base import JSONType
    from yandex_music.utils.request_async import Request


class LandingMixin(ClientBase):
    """Миксин для методов, связанных с лендингом и фидом."""

    _request: 'Request'

    @log
    async def feed(self, *args: Any, **kwargs: Any) -> Optional[Feed]:
        """Получение потока информации (фида) подобранного под пользователя. Содержит умные плейлисты.

        Args:
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.Feed` | :obj:`None`: Умные плейлисты пользователя или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/feed'

        result = await self._request.get(url, *args, **kwargs)

        return Feed.de_json(result, self)

    @log
    async def feed_wizard_is_passed(self, *args: Any, **kwargs: Any) -> bool:
        """Получение информации о прохождении визарда.

        Note:
            Временное событие на хэллоуин.

        Args:
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`bool`: Прошел ли пользователь визард или нет.
        """
        url = f'{self.base_url}/feed/wizard/is-passed'

        result = await self._request.get(url, *args, **kwargs)

        return result.get('isWizardPassed') or False

    @log
    async def landing(self, blocks: Union[str, List[str]], *args: Any, **kwargs: Any) -> Optional[Landing]:
        """Получение лендинг-страницы содержащий блоки с новыми релизами, чартами, плейлистами с новинками и т.д.

        Note:
            Поддерживаемые типы блоков: `personalplaylists`, `promotions`, `new-releases`, `new-playlists`, `mixes`,
            `chart`, `artists`, `albums`, `playlists`, `play_contexts`.

        Args:
            blocks (:obj:`str` | :obj:`list` из :obj:`str`): Блок или список блоков необходимых для выдачи.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.Landing` | :obj:`None`: Лендинг-страница или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/landing3'
        params = cast('JSONType', {'blocks': blocks, 'eitherUserId': '10254713668400548221'})

        result = await self._request.get(url, params, *args, **kwargs)
        # TODO (MarshalX) что тут делает константа с чьим-то User ID
        #  https://github.com/MarshalX/yandex-music-api/issues/553

        return Landing.de_json(result, self)

    @log
    async def chart(self, chart_option: str = '', *args: Any, **kwargs: Any) -> Optional[ChartInfo]:
        """Получение чарта.

        Note:
            `chart_option` - это постфикс к запросу из поля `menu` чарта.
            Например, на сайте можно выбрать глобальный (world) чарт или российский (russia).

        Args:
            chart_option (:obj:`str` optional): Параметры чарта.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.ChartInfo`: Чарт.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/landing3/chart'

        if chart_option:
            url = f'{url}/{chart_option}'

        result = await self._request.get(url, *args, **kwargs)

        return ChartInfo.de_json(result, self)

    @log
    async def new_releases(self, *args: Any, **kwargs: Any) -> Optional[LandingList]:
        """Получение полного списка всех новых релизов (альбомов).

        Args:
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.LandingList`: Список новых альбомов.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/landing3/new-releases'

        result = await self._request.get(url, *args, **kwargs)

        return LandingList.de_json(result, self)

    @log
    async def new_playlists(self, *args: Any, **kwargs: Any) -> Optional[LandingList]:
        """Получение полного списка всех новых плейлистов.

        Args:
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.LandingList`: Список новых плейлистов.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/landing3/new-playlists'

        result = await self._request.get(url, *args, **kwargs)

        return LandingList.de_json(result, self)

    @log
    async def podcasts(self, *args: Any, **kwargs: Any) -> Optional[LandingList]:
        """Получение подкастов с лендинга.

        Args:
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.LandingList`: Список подкастов.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/landing3/podcasts'

        result = await self._request.get(url, *args, **kwargs)

        return LandingList.de_json(result, self)

    @log
    async def genres(self, *args: Any, **kwargs: Any) -> List[Genre]:
        """Получение жанров музыки.

        Args:
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`list` из :obj:`yandex_music.Genre` | :obj:`None`: Жанры музыки или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/genres'

        result = await self._request.get(url, *args, **kwargs)

        return Genre.de_list(result, self)

    @log
    async def tags(self, tag_id: str, *args: Any, **kwargs: Any) -> Optional[TagResult]:
        """Получение тега (подборки).

        Note:
            Теги есть в `MixLink` у `Landing`, а также плейлистов в `.tags`.

            У `MixLink` есть `URL`, но `tag_id` только его последняя часть.
            Например, `/tag/belarus/`. `Tag` - `belarus`.

        Args:
            tag_id (:obj:`str`): Уникальный идентификатор тега.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
           :obj:`yandex_music.TagResult`: Тег с плейлистами.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/tags/{tag_id}/playlist-ids'

        result = await self._request.get(url, *args, **kwargs)

        return TagResult.de_json(result, self)

    # camelCase псевдонимы

    #: Псевдоним для :attr:`feed_wizard_is_passed`
    feedWizardIsPassed = feed_wizard_is_passed
    #: Псевдоним для :attr:`new_releases`
    newReleases = new_releases
    #: Псевдоним для :attr:`new_playlists`
    newPlaylists = new_playlists
