from typing import TYPE_CHECKING, Any, Optional

from yandex_music import Search, Suggestions
from yandex_music._client_async import log
from yandex_music._client_base import ClientBase
from yandex_music.exceptions import BadRequestError

if TYPE_CHECKING:
    from yandex_music.utils.request_async import Request


class SearchMixin(ClientBase):
    """Миксин для методов поиска."""

    _request: 'Request'

    @log
    async def search(
        self,
        text: str,
        nocorrect: bool = False,
        type_: str = 'all',
        page: int = 0,
        playlist_in_best: bool = True,
        *args: Any,
        **kwargs: Any,
    ) -> Optional[Search]:
        """Осуществление поиска по запросу и типу, получение результатов.

        Note:
            Известные значения для поля `type_`: `all`, `artist`, `user`, `album`, `playlist`, `track`, `podcast`,
            `podcast_episode`.

            При поиске `type=all` не возвращаются подкасты и эпизоды. Указывайте конкретный тип для поиска.

        Args:
            text (:obj:`str`): Текст запроса.
            nocorrect (:obj:`bool`): Если :obj:`False`, то ошибочный запрос будет исправлен. Например, запрос
                "Гражданская абарона" будет исправлен на "Гражданская оборона".
            type_ (:obj:`str`): Среди какого типа искать (трек, плейлист, альбом, исполнитель, пользователь, подкаст).
            page (:obj:`int`): Номер страницы.
            playlist_in_best (:obj:`bool`): Выдавать ли плейлисты лучшим вариантом поиска.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.Search` | :obj:`None`: Результаты поиска или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/search'

        params = {
            'text': text,
            'nocorrect': str(nocorrect),
            'type': type_,
            'page': page,
            'playlist-in-best': str(playlist_in_best),
        }

        result = await self._request.get(url, params, *args, **kwargs)

        if isinstance(result, str):
            raise BadRequestError(result)

        return Search.de_json(result, self)

    @log
    async def search_suggest(self, part: str, *args: Any, **kwargs: Any) -> Optional[Suggestions]:
        """Получение подсказок по введенной части поискового запроса.

        Args:
            part (:obj:`str`): Часть поискового запроса.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.Suggestions` | :obj:`None`: Подсказки для запроса или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/search/suggest'

        result = await self._request.get(url, {'part': part}, *args, **kwargs)

        return Suggestions.de_json(result, self)

    # camelCase псевдонимы

    #: Псевдоним для :attr:`search_suggest`
    searchSuggest = search_suggest
