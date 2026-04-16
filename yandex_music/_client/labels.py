###############################################################################################
# THIS IS AUTO GENERATED COPY OF yandex_music/_client_async/labels.py. DON'T EDIT IT BY HANDS #
###############################################################################################

from typing import TYPE_CHECKING, Any, Optional, Union

from yandex_music import Label, LabelAlbums, LabelArtists
from yandex_music._client import log
from yandex_music._client_base import ClientBase

if TYPE_CHECKING:
    from yandex_music.utils.request import Request


class LabelsMixin(ClientBase):
    """Лейблы.

    Миксин для методов, связанных с лейблами.
    """

    _request: 'Request'

    @log
    def label(self, label_id: Union[str, int], *args: Any, **kwargs: Any) -> Optional[Label]:
        """Получение информации о лейбле.

        Args:
            label_id (:obj:`str` | :obj:`int`): Уникальный идентификатор лейбла.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.Label` | :obj:`None`: Информация о лейбле или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/labels/{label_id}'

        result = self._request.get(url, *args, **kwargs)

        return Label.de_json(result, self)

    @log
    def label_albums(
        self,
        label_id: Union[str, int],
        page: int = 0,
        page_size: int = 100,
        sort_by: Optional[str] = None,
        sort_order: Optional[str] = None,
        *args: Any,
        **kwargs: Any,
    ) -> Optional[LabelAlbums]:
        """Получение альбомов лейбла.

        Note:
            Известные значения для `sort_by`: `year`, `rating`.
            Известные значения для `sort_order`: `asc`, `desc`.

        Args:
            label_id (:obj:`str` | :obj:`int`): Уникальный идентификатор лейбла.
            page (:obj:`int`, optional): Номер страницы.
            page_size (:obj:`int`, optional): Количество альбомов на странице.
            sort_by (:obj:`str`, optional): Параметр для сортировки.
            sort_order (:obj:`str`, optional): Порядок сортировки.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.LabelAlbums` | :obj:`None`: Страница списка альбомов лейбла или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/labels/{label_id}/albums'

        params: dict = {'page': page, 'pageSize': page_size}
        if sort_by is not None:
            params['sortBy'] = sort_by
        if sort_order is not None:
            params['sortOrder'] = sort_order

        result = self._request.get(url, params, *args, **kwargs)

        return LabelAlbums.de_json(result, self)

    @log
    def label_artists(
        self,
        label_id: Union[str, int],
        page: int = 0,
        page_size: int = 100,
        *args: Any,
        **kwargs: Any,
    ) -> Optional[LabelArtists]:
        """Получение артистов лейбла.

        Args:
            label_id (:obj:`str` | :obj:`int`): Уникальный идентификатор лейбла.
            page (:obj:`int`, optional): Номер страницы.
            page_size (:obj:`int`, optional): Количество артистов на странице.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.LabelArtists` | :obj:`None`: Страница списка артистов лейбла или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/labels/{label_id}/artists'

        params = {'page': page, 'pageSize': page_size}

        result = self._request.get(url, params, *args, **kwargs)

        return LabelArtists.de_json(result, self)

    # camelCase псевдонимы

    #: Псевдоним для :attr:`label_albums`
    labelAlbums = label_albums
    #: Псевдоним для :attr:`label_artists`
    labelArtists = label_artists
