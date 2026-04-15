################################################################################################
# THIS IS AUTO GENERATED COPY OF yandex_music/_client_async/credits.py. DON'T EDIT IT BY HANDS #
################################################################################################

from typing import TYPE_CHECKING, Any, Optional, Union

from yandex_music import Credits
from yandex_music._client import log
from yandex_music._client_base import ClientBase

if TYPE_CHECKING:
    from yandex_music.utils.request import Request


class CreditsMixin(ClientBase):
    """Миксин для методов, связанных с получением участников создания контента."""

    _request: 'Request'

    def _get_credits(
        self,
        entity_type: str,
        entity_id: Union[str, int],
        *args: Any,
        **kwargs: Any,
    ) -> Optional[Credits]:
        """Получение информации об участниках создания контента.

        Note:
            Известные типы сущностей: ``tracks``, ``clips``.

        Args:
            entity_type (:obj:`str`): Тип сущности (``tracks``, ``clips``).
            entity_id (:obj:`str` | :obj:`int`): Уникальный идентификатор сущности.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.Credits` | :obj:`None`: Участники создания контента или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/{entity_type}/{entity_id}/credits'

        result = self._request.get(url, *args, **kwargs)

        return Credits.de_json(result, self)

    @log
    def tracks_credits(self, track_id: Union[str, int], *args: Any, **kwargs: Any) -> Optional[Credits]:
        """Получение информации об участниках создания трека.

        Args:
            track_id (:obj:`str` | :obj:`int`): Уникальный идентификатор трека.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.Credits` | :obj:`None`: Участники создания трека или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        return self._get_credits('tracks', track_id, *args, **kwargs)

    @log
    def clips_credits(self, clip_id: Union[str, int], *args: Any, **kwargs: Any) -> Optional[Credits]:
        """Получение информации об участниках создания клипа.

        Args:
            clip_id (:obj:`str` | :obj:`int`): Уникальный идентификатор клипа.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.Credits` | :obj:`None`: Участники создания клипа или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        return self._get_credits('clips', clip_id, *args, **kwargs)

    # camelCase псевдонимы

    #: Псевдоним для :attr:`tracks_credits`
    tracksCredits = tracks_credits
    #: Псевдоним для :attr:`clips_credits`
    clipsCredits = clips_credits
