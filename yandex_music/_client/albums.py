###############################################################################################
# THIS IS AUTO GENERATED COPY OF yandex_music/_client_async/albums.py. DON'T EDIT IT BY HANDS #
###############################################################################################

from typing import TYPE_CHECKING, Any, List, Optional, Union

from yandex_music import Album, AlbumTrailer, SimilarEntityItem
from yandex_music._client import log
from yandex_music._client_base import ClientBase, is_dict

if TYPE_CHECKING:
    from yandex_music.utils.request import Request


class AlbumsMixin(ClientBase):
    """Миксин для методов, связанных с альбомами."""

    _request: 'Request'

    @log
    def albums_with_tracks(self, album_id: Union[str, int], *args: Any, **kwargs: Any) -> Optional[Album]:
        """Получение альбома по его уникальному идентификатору вместе с треками.

        Args:
            album_id (:obj:`str` | :obj:`int`): Уникальный идентификатор альбома.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`list` из :obj:`yandex_music.Album` | :obj:`None`: Альбом или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/albums/{album_id}/with-tracks'

        result = self._request.get(url, *args, **kwargs)

        return Album.de_json(result, self)

    @log
    def albums_disclaimer(self, album_id: Union[str, int], *args: Any, **kwargs: Any) -> Optional[str]:
        """Получение дисклеймера альбома.

        Args:
            album_id (:obj:`str` | :obj:`int`): Уникальный идентификатор альбома.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`str` | :obj:`None`: Текст дисклеймера или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/albums/{album_id}/disclaimer'

        result = self._request.get(url, *args, **kwargs)

        if is_dict(result):
            return result.get('text')
        return None

    @log
    def albums_similar_entities(self, album_id: Union[str, int], *args: Any, **kwargs: Any) -> List[SimilarEntityItem]:
        """Получение похожих сущностей для альбома.

        Args:
            album_id (:obj:`str` | :obj:`int`): Уникальный идентификатор альбома.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`list` из :obj:`yandex_music.SimilarEntityItem`: Список похожих сущностей.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/albums/{album_id}/similar-entities'

        result = self._request.get(url, *args, **kwargs)

        if is_dict(result):
            return list(SimilarEntityItem.de_list(result.get('items'), self))
        return []

    @log
    def albums_trailer(self, album_id: Union[str, int], *args: Any, **kwargs: Any) -> Optional[AlbumTrailer]:
        """Получение трейлера альбома.

        Args:
            album_id (:obj:`str` | :obj:`int`): Уникальный идентификатор альбома.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.AlbumTrailer` | :obj:`None`: Трейлер альбома или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/albums/{album_id}/trailer'

        result = self._request.get(url, *args, **kwargs)

        return AlbumTrailer.de_json(result, self)

    # camelCase псевдонимы

    #: Псевдоним для :attr:`albums_with_tracks`
    albumsWithTracks = albums_with_tracks
    #: Псевдоним для :attr:`albums_disclaimer`
    albumsDisclaimer = albums_disclaimer
    #: Псевдоним для :attr:`albums_similar_entities`
    albumsSimilarEntities = albums_similar_entities
    #: Псевдоним для :attr:`albums_trailer`
    albumsTrailer = albums_trailer
