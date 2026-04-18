###############################################################################################
# THIS IS AUTO GENERATED COPY OF yandex_music/_client_async/_batch.py. DON'T EDIT IT BY HANDS #
###############################################################################################

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Sequence, Union, overload

from typing_extensions import Literal

from yandex_music import Album, Artist, Playlist, Track
from yandex_music._client_base import ClientBase, de_list

if TYPE_CHECKING:
    from yandex_music.utils.request import Request


class _BatchMixin(ClientBase):
    """Внутренний миксин с общим помощником для пакетных запросов."""

    _request: 'Request'

    @overload
    def _get_list(
        self,
        object_type: Literal['artist'],
        ids: Union[Sequence[Union[str, int]], int, str],
        params: Optional[Dict[str, Any]] = ...,
        *args: Any,
        **kwargs: Any,
    ) -> List[Artist]: ...

    @overload
    def _get_list(
        self,
        object_type: Literal['album'],
        ids: Union[Sequence[Union[str, int]], int, str],
        params: Optional[Dict[str, Any]] = ...,
        *args: Any,
        **kwargs: Any,
    ) -> List[Album]: ...

    @overload
    def _get_list(
        self,
        object_type: Literal['track'],
        ids: Union[Sequence[Union[str, int]], int, str],
        params: Optional[Dict[str, Any]] = ...,
        *args: Any,
        **kwargs: Any,
    ) -> List[Track]: ...

    @overload
    def _get_list(
        self,
        object_type: Literal['playlist'],
        ids: Union[Sequence[Union[str, int]], int, str],
        params: Optional[Dict[str, Any]] = ...,
        *args: Any,
        **kwargs: Any,
    ) -> List[Playlist]: ...

    def _get_list(
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

        result = self._request.post(url, params, *args, **kwargs)

        return list(de_list[object_type](result, self))
