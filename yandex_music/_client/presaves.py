#################################################################################################
# THIS IS AUTO GENERATED COPY OF yandex_music/_client_async/presaves.py. DON'T EDIT IT BY HANDS #
#################################################################################################

from typing import TYPE_CHECKING, Any, Optional, Union

from yandex_music import Presaves
from yandex_music._client import log
from yandex_music._client_base import ClientBase, UserIdType

if TYPE_CHECKING:
    from yandex_music.utils.request import Request


class PresavesMixin(ClientBase):
    """Предсохранения.

    Миксин для методов, связанных с предсохранениями альбомов.
    """

    _request: 'Request'

    @log
    def users_presaves(
        self,
        include_released: bool = False,
        include_upcoming: bool = True,
        user_id: UserIdType = None,
        *args: Any,
        **kwargs: Any,
    ) -> Optional[Presaves]:
        """Получение списка предсохранённых альбомов.

        Args:
            include_released (:obj:`bool`, optional): Включить вышедшие альбомы.
            include_upcoming (:obj:`bool`, optional): Включить предстоящие альбомы.
            user_id (:obj:`str` | :obj:`int`, optional): Уникальный идентификатор пользователя. Если не указан
                используется ID текущего пользователя.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.Presaves` | :obj:`None`: Список предсохранённых альбомов или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        if user_id is None and self.account_uid is not None:
            user_id = self.account_uid

        url = f'{self.base_url}/users/{user_id}/presaves'

        params = {
            'includeReleased': str(include_released).lower(),
            'includeUpcoming': str(include_upcoming).lower(),
        }

        result = self._request.get(url, params, *args, **kwargs)

        return Presaves.de_json(result, self)

    @log
    def users_presaves_add(
        self,
        album_id: Union[str, int],
        like_after_release: bool = True,
        user_id: UserIdType = None,
        *args: Any,
        **kwargs: Any,
    ) -> bool:
        """Предсохранение альбома.

        Args:
            album_id (:obj:`str` | :obj:`int`): Уникальный идентификатор альбома.
            like_after_release (:obj:`bool`, optional): Автоматически поставить лайк после выхода альбома.
            user_id (:obj:`str` | :obj:`int`, optional): Уникальный идентификатор пользователя. Если не указан
                используется ID текущего пользователя.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`bool`: :obj:`True` при успешном выполнении запроса, иначе :obj:`False`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        if user_id is None and self.account_uid is not None:
            user_id = self.account_uid

        url = f'{self.base_url}/users/{user_id}/presaves/add'

        params = {
            'albumId': album_id,
            'likeAfterRelease': str(like_after_release).lower(),
        }

        result = self._request.post(url, params, *args, **kwargs)

        return result == 'ok'

    @log
    def users_presaves_remove(
        self,
        album_id: Union[str, int],
        user_id: UserIdType = None,
        *args: Any,
        **kwargs: Any,
    ) -> bool:
        """Удаление предсохранения альбома.

        Args:
            album_id (:obj:`str` | :obj:`int`): Уникальный идентификатор альбома.
            user_id (:obj:`str` | :obj:`int`, optional): Уникальный идентификатор пользователя. Если не указан
                используется ID текущего пользователя.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`bool`: :obj:`True` при успешном выполнении запроса, иначе :obj:`False`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        if user_id is None and self.account_uid is not None:
            user_id = self.account_uid

        url = f'{self.base_url}/users/{user_id}/presaves/remove'

        params = {
            'albumId': album_id,
        }

        result = self._request.post(url, params, *args, **kwargs)

        return result == 'ok'

    # camelCase псевдонимы

    #: Псевдоним для :attr:`users_presaves`
    usersPresaves = users_presaves
    #: Псевдоним для :attr:`users_presaves_add`
    usersPresavesAdd = users_presaves_add
    #: Псевдоним для :attr:`users_presaves_remove`
    usersPresavesRemove = users_presaves_remove
