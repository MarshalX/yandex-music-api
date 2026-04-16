from typing import TYPE_CHECKING, Any, Dict, List, Optional, Sequence, Union, overload

from typing_extensions import Literal

from yandex_music import Album, Artist, Playlist, Track
from yandex_music._client_async import log
from yandex_music._client_base import ClientBase, de_list

if TYPE_CHECKING:
    from yandex_music.utils.request_async import Request


class BatchMixin(ClientBase):
    """Пакетные запросы.

    Миксин для методов пакетного получения объектов.
    """

    _request: 'Request'

    @overload
    async def _get_list(
        self,
        object_type: Literal['artist'],
        ids: Union[Sequence[Union[str, int]], int, str],
        params: Optional[Dict[str, Any]] = ...,
        *args: Any,
        **kwargs: Any,
    ) -> List[Artist]: ...

    @overload
    async def _get_list(
        self,
        object_type: Literal['album'],
        ids: Union[Sequence[Union[str, int]], int, str],
        params: Optional[Dict[str, Any]] = ...,
        *args: Any,
        **kwargs: Any,
    ) -> List[Album]: ...

    @overload
    async def _get_list(
        self,
        object_type: Literal['track'],
        ids: Union[Sequence[Union[str, int]], int, str],
        params: Optional[Dict[str, Any]] = ...,
        *args: Any,
        **kwargs: Any,
    ) -> List[Track]: ...

    @overload
    async def _get_list(
        self,
        object_type: Literal['playlist'],
        ids: Union[Sequence[Union[str, int]], int, str],
        params: Optional[Dict[str, Any]] = ...,
        *args: Any,
        **kwargs: Any,
    ) -> List[Playlist]: ...

    async def _get_list(
        self,
        object_type: str,
        ids: Union[Sequence[Union[str, int]], int, str],
        params: Optional[Dict[str, Any]] = None,
        *args: Any,
        **kwargs: Any,
    ) -> list:
        """Получение объекта/объектов.

        Args:
            object_type (:obj:`str`): Тип объекта.
            ids (:obj:`str` | :obj:`int` | :obj:`list` из :obj:`str` | :obj:`list` из :obj:`int`): Уникальный
                идентификатор объекта или объектов.
            params (:obj:`dict`, optional): Параметры, которые будут переданы в запрос.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`list` из :obj:`yandex_music.Artist` | :obj:`list` из :obj:`yandex_music.Album` |
                :obj:`list` из :obj:`yandex_music.Track` | :obj:`list` из :obj:`yandex_music.Playlist`: Запрошенный
                объект.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        if params is None:
            params = {}
        params.update({f'{object_type}-ids': ids})

        url = f'{self.base_url}/{object_type}s' + ('/list' if object_type == 'playlist' else '')

        result = await self._request.post(url, params, *args, **kwargs)

        return list(de_list[object_type](result, self))

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
    async def albums(self, album_ids: Union[List[Union[str, int]], int, str], *args: Any, **kwargs: Any) -> List[Album]:
        """Получение альбома/альбомов.

        Args:
            album_ids (:obj:`str` | :obj:`int` | :obj:`list` из :obj:`str` | :obj:`list` из :obj:`int`): Уникальный
                идентификатор альбома или альбомов.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`list` из :obj:`yandex_music.Album`: Альбом или альбомы.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        return await self._get_list('album', album_ids, *args, **kwargs)

    @log
    async def tracks(
        self,
        track_ids: Union[Sequence[Union[str, int]], int, str],
        with_positions: bool = True,
        *args: Any,
        **kwargs: Any,
    ) -> List[Track]:
        """Получение трека/треков.

        Args:
            track_ids (:obj:`str` | :obj:`int` | :obj:`list` из :obj:`str` | :obj:`list` из :obj:`int`): Уникальный
                идентификатор трека или треков.
            with_positions (:obj:`bool`, optional): С позициями TODO.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`list` из :obj:`yandex_music.Track`: Трек или Треки.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        return await self._get_list('track', track_ids, {'with-positions': str(with_positions)}, *args, **kwargs)

    @log
    async def playlists_list(
        self, playlist_ids: Union[List[Union[str, int]], int, str], *args: Any, **kwargs: Any
    ) -> List[Playlist]:
        """Получение плейлиста/плейлистов.

        Note:
            Идентификатор плейлиста указывается в формате `owner_id:playlist_id`. Где `playlist_id` - идентификатор
            плейлиста, `owner_id` - уникальный идентификатор владельца плейлиста.

            Данный метод возвращает сокращенную модель плейлиста для отображения больших список.

        Warning:
            Данный метод не возвращает список треков у плейлиста! Для получения объекта :obj:`yandex_music.Playlist` c
            заполненным полем `tracks` используйте метод :func:`yandex_music.ClientAsync.users_playlists` или
            метод :func:`yandex_music.Playlist.fetch_tracks`.

        Args:
            playlist_ids (:obj:`str` | :obj:`int` | :obj:`list` из :obj:`str` | :obj:`list` из :obj:`int`): Уникальный
                идентификатор плейлиста или плейлистов.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`list` из :obj:`yandex_music.Playlist`: Плейлист или плейлисты.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        return await self._get_list('playlist', playlist_ids, *args, **kwargs)

    # camelCase псевдонимы

    #: Псевдоним для :attr:`playlists_list`
    playlistsList = playlists_list
