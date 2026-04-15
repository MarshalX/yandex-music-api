from typing import TYPE_CHECKING, Any, Optional, Union

from yandex_music import Disclaimer
from yandex_music._client_async import log
from yandex_music._client_base import ClientBase

if TYPE_CHECKING:
    from yandex_music.utils.request_async import Request


class DisclaimersMixin(ClientBase):
    """Миксин для методов, связанных с получением дисклеймеров контента."""

    _request: 'Request'

    async def _get_disclaimer(
        self,
        entity_type: str,
        entity_id: Union[str, int],
        *args: Any,
        **kwargs: Any,
    ) -> Optional[Disclaimer]:
        """Получение дисклеймера контента.

        Note:
            Известные типы сущностей: ``tracks``, ``clips``, ``albums``, ``artists``.

        Args:
            entity_type (:obj:`str`): Тип сущности (``tracks``, ``clips``, ``albums``).
            entity_id (:obj:`str` | :obj:`int`): Уникальный идентификатор сущности.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.Disclaimer` | :obj:`None`: Дисклеймер контента или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/{entity_type}/{entity_id}/disclaimer'

        result = await self._request.get(url, *args, **kwargs)

        return Disclaimer.de_json(result, self)

    @log
    async def tracks_disclaimer(self, track_id: Union[str, int], *args: Any, **kwargs: Any) -> Optional[Disclaimer]:
        """Получение дисклеймера трека.

        Args:
            track_id (:obj:`str` | :obj:`int`): Уникальный идентификатор трека.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.Disclaimer` | :obj:`None`: Дисклеймер трека или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        return await self._get_disclaimer('tracks', track_id, *args, **kwargs)

    @log
    async def clips_disclaimer(self, clip_id: Union[str, int], *args: Any, **kwargs: Any) -> Optional[Disclaimer]:
        """Получение дисклеймера клипа.

        Args:
            clip_id (:obj:`str` | :obj:`int`): Уникальный идентификатор клипа.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.Disclaimer` | :obj:`None`: Дисклеймер клипа или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        return await self._get_disclaimer('clips', clip_id, *args, **kwargs)

    @log
    async def albums_disclaimer(self, album_id: Union[str, int], *args: Any, **kwargs: Any) -> Optional[Disclaimer]:
        """Получение дисклеймера альбома.

        Args:
            album_id (:obj:`str` | :obj:`int`): Уникальный идентификатор альбома.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.Disclaimer` | :obj:`None`: Дисклеймер альбома или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        return await self._get_disclaimer('albums', album_id, *args, **kwargs)

    @log
    async def artists_disclaimer(self, artist_id: Union[str, int], *args: Any, **kwargs: Any) -> Optional[Disclaimer]:
        """Получение дисклеймера артиста.

        Args:
            artist_id (:obj:`str` | :obj:`int`): Уникальный идентификатор артиста.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.Disclaimer` | :obj:`None`: Дисклеймер артиста или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        return await self._get_disclaimer('artists', artist_id, *args, **kwargs)

    # camelCase псевдонимы

    #: Псевдоним для :attr:`tracks_disclaimer`
    tracksDisclaimer = tracks_disclaimer
    #: Псевдоним для :attr:`clips_disclaimer`
    clipsDisclaimer = clips_disclaimer
    #: Псевдоним для :attr:`albums_disclaimer`
    albumsDisclaimer = albums_disclaimer
    #: Псевдоним для :attr:`artists_disclaimer`
    artistsDisclaimer = artists_disclaimer
