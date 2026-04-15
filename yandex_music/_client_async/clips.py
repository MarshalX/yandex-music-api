from typing import TYPE_CHECKING, Any, List, Optional, Union

from yandex_music import Clip, ClipsWillLike
from yandex_music._client_async import log
from yandex_music._client_base import ClientBase

if TYPE_CHECKING:
    from yandex_music.utils.request_async import Request


class ClipsMixin(ClientBase):
    """Миксин для методов, связанных с видеоклипами."""

    _request: 'Request'

    @log
    async def clips(self, clip_ids: Union[List[Union[str, int]], str, int], *args: Any, **kwargs: Any) -> List[Clip]:
        """Получение клипов по идентификаторам.

        Args:
            clip_ids (:obj:`str` | :obj:`int` | :obj:`list`): Уникальный идентификатор клипа или список идентификаторов.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`list` из :obj:`yandex_music.Clip`: Список клипов.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/clips'

        if isinstance(clip_ids, list):
            clip_ids = ','.join(map(str, clip_ids))

        params = {'clipIds': clip_ids}

        result = await self._request.get(url, params, *args, **kwargs)

        return list(Clip.de_list(result, self))

    @log
    async def clips_will_like(
        self,
        page: int = 0,
        page_size: int = 50,
        *args: Any,
        **kwargs: Any,
    ) -> Optional[ClipsWillLike]:
        """Получение подборки рекомендуемых клипов.

        Args:
            page (:obj:`int`, optional): Номер страницы.
            page_size (:obj:`int`, optional): Количество клипов на странице.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.ClipsWillLike` | :obj:`None`: Подборка рекомендуемых клипов или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/clips/will/like'

        params = {
            'page': page,
            'pageSize': page_size,
        }

        result = await self._request.get(url, params, *args, **kwargs)

        return ClipsWillLike.de_json(result, self)

    # camelCase псевдонимы

    #: Псевдоним для :attr:`clips_will_like`
    clipsWillLike = clips_will_like
