##############################################################################################
# THIS IS AUTO GENERATED COPY OF yandex_music/_client_async/batch.py. DON'T EDIT IT BY HANDS #
##############################################################################################

from typing import TYPE_CHECKING, Any, List, Optional, Union

from yandex_music import Album, Artist, Playlist, Track
from yandex_music._client import log
from yandex_music._client_base import ClientBase, de_list

if TYPE_CHECKING:
    from yandex_music.base import JSONType
    from yandex_music.utils.request import Request


class BatchMixin(ClientBase):
    """Миксин для методов пакетного получения объектов."""

    _request: 'Request'

    def _get_list(
        self,
        object_type: str,
        ids: Union[List[Union[str, int]], int, str],
        params: Optional['JSONType'] = None,
        *args: Any,
        **kwargs: Any,
    ) -> List[Union[Artist, Album, Track, Playlist]]:
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

        result = self._request.post(url, params, *args, **kwargs)

        return de_list[object_type](result, self)

    @log
    def artists(self, artist_ids: Union[List[Union[str, int]], int, str], *args: Any, **kwargs: Any) -> List[Artist]:
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
        return self._get_list('artist', artist_ids, *args, **kwargs)

    @log
    def albums(self, album_ids: Union[List[Union[str, int]], int, str], *args: Any, **kwargs: Any) -> List[Album]:
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
        return self._get_list('album', album_ids, *args, **kwargs)

    @log
    def tracks(
        self,
        track_ids: Union[List[str], List[int], List[Union[str, int]], int, str],
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
        return self._get_list('track', track_ids, {'with-positions': str(with_positions)}, *args, **kwargs)

    @log
    def playlists_list(
        self, playlist_ids: Union[List[Union[str, int]], int, str], *args: Any, **kwargs: Any
    ) -> List[Playlist]:
        """Получение плейлиста/плейлистов.

        Note:
            Идентификатор плейлиста указывается в формате `owner_id:playlist_id`. Где `playlist_id` - идентификатор
            плейлиста, `owner_id` - уникальный идентификатор владельца плейлиста.

            Данный метод возвращает сокращенную модель плейлиста для отображения больших список.

        Warning:
            Данный метод не возвращает список треков у плейлиста! Для получения объекта :obj:`yandex_music.Playlist` c
            заполненным полем `tracks` используйте метод :func:`yandex_music.Client.users_playlists` или
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
        return self._get_list('playlist', playlist_ids, *args, **kwargs)

    # camelCase псевдонимы

    #: Псевдоним для :attr:`playlists_list`
    playlistsList = playlists_list
