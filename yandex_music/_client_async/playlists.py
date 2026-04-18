from typing import TYPE_CHECKING, Any, List, Optional, Union

from yandex_music import (
    GeneratedPlaylist,
    Playlist,
    PlaylistRecommendations,
    PlaylistSimilarEntities,
    PlaylistsList,
    PlaylistTrailer,
    UserSettings,
)
from yandex_music._client_async import log
from yandex_music._client_async._batch import _BatchMixin
from yandex_music._client_base import UserIdType, is_dict
from yandex_music.utils.difference import Difference

if TYPE_CHECKING:
    from yandex_music.utils.request_async import Request


class PlaylistsMixin(_BatchMixin):
    """Плейлисты.

    Миксин для методов, связанных с плейлистами.
    """

    _request: 'Request'

    @log
    async def users_settings(self, user_id: UserIdType = None, *args: Any, **kwargs: Any) -> Optional[UserSettings]:
        """Получение настроек пользователя.

        Note:
            Для получения настроек пользователя нужно быть авторизованным или владеть `user_id`.

        Args:
            user_id (:obj:`str` | :obj:`int`, optional): Уникальный идентификатор пользователя чьи настройки хотим
                получить.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.UserSettings` | :obj:`None`: Настройки пользователя или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        if user_id is None and self.account_uid is not None:
            user_id = self.account_uid

        url = f'{self.base_url}/users/{user_id}/settings'

        result = await self._request.get(url, *args, **kwargs)

        if is_dict(result):
            return UserSettings.de_json(result.get('userSettings'), self)
        return None

    @log
    async def users_playlists(
        self,
        kind: Union[List[Union[str, int]], str, int],
        user_id: UserIdType = None,
        *args: Any,
        **kwargs: Any,
    ) -> Union[Playlist, List[Playlist], None]:
        """Получение плейлиста или списка плейлистов по уникальным идентификаторам.

        Note:
            Если передан один `kind`, то вернётся не список плейлистов, а один плейлист.

        Args:
            kind (:obj:`str` | :obj:`int` | :obj:`list` из :obj:`str` | :obj:`int`): Уникальный идентификатор плейлиста
                или их список.
            user_id (:obj:`str` | :obj:`int`, optional): Уникальный идентификатор пользователя владеющим плейлистом.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`list` из :obj:`yandex_music.Playlist` | :obj:`yandex_music.Playlist` | :obj:`None`:
            Список плейлистов или плейлист, иначе :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        if user_id is None and self.account_uid is not None:
            user_id = self.account_uid

        if isinstance(kind, list):
            url = f'{self.base_url}/users/{user_id}/playlists'

            data = {'kinds': kind}

            result = await self._request.post(url, data, *args, **kwargs)
            return list(Playlist.de_list(result, self))

        url = f'{self.base_url}/users/{user_id}/playlists/{kind}'
        result = await self._request.get(url, *args, **kwargs)
        return Playlist.de_json(result, self)

    @log
    async def users_playlists_recommendations(
        self, kind: Union[str, int], user_id: UserIdType = None, *args: Any, **kwargs: Any
    ) -> Optional[PlaylistRecommendations]:
        """Получение рекомендаций для плейлиста.

        Args:
            kind (:obj:`str` | :obj:`int`): Уникальный идентификатор плейлиста.
            user_id (:obj:`str` | :obj:`int`): Уникальный идентификатор пользователя владеющим плейлистом.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.PlaylistRecommendations` | :obj:`None`: Рекомендации для плейлиста или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        if user_id is None and self.account_uid is not None:
            user_id = self.account_uid

        url = f'{self.base_url}/users/{user_id}/playlists/{kind}/recommendations'

        result = await self._request.get(url, *args, **kwargs)

        return PlaylistRecommendations.de_json(result, self)

    @log
    async def users_playlists_create(
        self,
        title: str,
        visibility: str = 'public',
        user_id: UserIdType = None,
        *args: Any,
        **kwargs: Any,
    ) -> Optional[Playlist]:
        """Создание плейлиста.

        Args:
            title (:obj:`str`): Название.
            visibility (:obj:`str`, optional): Модификатор доступа.
            user_id (:obj:`str` | :obj:`int`, optional): Уникальный идентификатор пользователя владеющим плейлистом.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.Playlist` | :obj:`None`: Созданный плейлист или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        if user_id is None and self.account_uid is not None:
            user_id = self.account_uid

        url = f'{self.base_url}/users/{user_id}/playlists/create'

        data = {'title': title, 'visibility': visibility}

        result = await self._request.post(url, data, *args, **kwargs)

        return Playlist.de_json(result, self)

    @log
    async def users_playlists_delete(
        self, kind: Union[str, int], user_id: UserIdType = None, *args: Any, **kwargs: Any
    ) -> bool:
        """Удаление плейлиста.

        Args:
            kind (:obj:`str` | :obj:`int`): Уникальный идентификатор плейлиста.
            user_id (:obj:`str` | :obj:`int`, optional): Уникальный идентификатор пользователя владеющим плейлистом.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`bool`: :obj:`True` при успешном выполнении запроса, иначе :obj:`False`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        if user_id is None and self.account_uid is not None:
            user_id = self.account_uid

        url = f'{self.base_url}/users/{user_id}/playlists/{kind}/delete'

        result = await self._request.post(url, *args, **kwargs)

        return result == 'ok'

    @log
    async def users_playlists_name(
        self,
        kind: Union[str, int],
        name: str,
        user_id: UserIdType = None,
        *args: Any,
        **kwargs: Any,
    ) -> Optional[Playlist]:
        """Изменение названия плейлиста.

        Args:
            kind (:obj:`str` | :obj:`int`): Уникальный идентификатор плейлиста.
            name (:obj:`str`): Новое название.
            user_id (:obj:`str` | :obj:`int`, optional): Уникальный идентификатор пользователя владеющим плейлистом.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.Playlist` | :obj:`None`: Изменённый плейлист или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        if user_id is None and self.account_uid is not None:
            user_id = self.account_uid

        url = f'{self.base_url}/users/{user_id}/playlists/{kind}/name'

        result = await self._request.post(url, {'value': name}, *args, **kwargs)

        return Playlist.de_json(result, self)

    @log
    async def users_playlists_visibility(
        self,
        kind: Union[str, int],
        visibility: str,
        user_id: UserIdType = None,
        *args: Any,
        **kwargs: Any,
    ) -> Optional[Playlist]:
        """Изменение видимости плейлиста.

        Note:
            Видимость (`visibility`) может быть задана только одним из двух значений: `private`, `public`.

        Args:
            kind (:obj:`str` | :obj:`int`): Уникальный идентификатор плейлиста.
            visibility (:obj:`str`): Новое название.
            user_id (:obj:`str` | :obj:`int`, optional): Уникальный идентификатор пользователя владеющим плейлистом.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.Playlist` | :obj:`None`: Изменённый плейлист или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        if user_id is None and self.account_uid is not None:
            user_id = self.account_uid

        url = f'{self.base_url}/users/{user_id}/playlists/{kind}/visibility'

        result = await self._request.post(url, {'value': visibility}, *args, **kwargs)

        return Playlist.de_json(result, self)

    @log
    async def users_playlists_change(
        self,
        kind: Union[str, int],
        diff: str,
        revision: int = 1,
        user_id: UserIdType = None,
        *args: Any,
        **kwargs: Any,
    ) -> Optional[Playlist]:
        """Изменение плейлиста.

        Note:
            Для получения отличий есть вспомогательный класс :class:`yandex_music.utils.difference.Difference`.

            Так же существуют уже готовые методы-обёртки над операциями.

        Args:
            kind (:obj:`str` | :obj:`int`): Уникальный идентификатор плейлиста.
            revision (:obj:`int`): TODO.
            diff (:obj:`str`): JSON представления отличий старого и нового плейлиста.
            user_id (:obj:`str` | :obj:`int`, optional): Уникальный идентификатор пользователя владеющим плейлистом.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.Playlist`: Изменённый плейлист или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        if user_id is None and self.account_uid is not None:
            user_id = self.account_uid

        url = f'{self.base_url}/users/{user_id}/playlists/{kind}/change'

        data = {'kind': kind, 'revision': revision, 'diff': diff}

        result = await self._request.post(url, data, *args, **kwargs)

        return Playlist.de_json(result, self)

    @log
    async def users_playlists_insert_track(
        self,
        kind: Union[str, int],
        track_id: Union[str, int],
        album_id: Union[str, int],
        at: int = 0,
        revision: int = 1,
        user_id: UserIdType = None,
        *args: Any,
        **kwargs: Any,
    ) -> Optional[Playlist]:
        """Добавление трека в плейлист.

        Note:
            Трек можно вставить с любое место плейлиста задав индекс вставки (аргумент `at`).

        Args:
            kind (:obj:`str` | :obj:`int`): Уникальный идентификатор плейлиста.
            track_id (:obj:`str` | :obj:`int`): Уникальный идентификатор трека.
            album_id (:obj:`str` | :obj:`int`): Уникальный идентификатор альбома.
            at (:obj:`int`): Индекс для вставки.
            revision (:obj:`int`): TODO.
            user_id (:obj:`str` | :obj:`int`, optional): Уникальный идентификатор пользователя владеющим плейлистом.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.Playlist`: Изменённый плейлист или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        if user_id is None and self.account_uid is not None:
            user_id = self.account_uid

        diff = Difference().add_insert(at, {'id': track_id, 'album_id': album_id})

        return await self.users_playlists_change(kind, diff.to_json(), revision, user_id, *args, **kwargs)

    @log
    async def users_playlists_delete_track(
        self,
        kind: Union[str, int],
        from_: int,
        to: int,
        revision: int = 1,
        user_id: UserIdType = None,
        *args: Any,
        **kwargs: Any,
    ) -> Optional[Playlist]:
        """Удаление треков из плейлиста.

        Note:
            Для удаление необходимо указать границы с какого по какой элемент (трек) удалить.

        Args:
            kind (:obj:`str` | :obj:`int`): Уникальный идентификатор плейлиста.
            from_ (:obj:`int`): С какого индекса.
            to (:obj:`int`): По какой индекс.
            revision (:obj:`int`): TODO.
            user_id (:obj:`str` | :obj:`int`, optional): Уникальный идентификатор пользователя владеющим плейлистом.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.Playlist` | :obj:`None`: Изменённый плейлист или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        if user_id is None and self.account_uid is not None:
            user_id = self.account_uid

        diff = Difference().add_delete(from_, to)

        return await self.users_playlists_change(kind, diff.to_json(), revision, user_id, *args, **kwargs)

    @log
    async def playlists_collective_join(self, user_id: int, token: str, **kwargs: Any) -> bool:
        """Присоединение к плейлисту как соавтор.

        Note:
            В качестве `user_id` принимается исключительно числовой уникальный идентификатор пользователя, не username.

            Токен можно получить в Web-версии. Для этого, на странице плейлиста нужно нажать на
            "Добавить соавтора". В полученной ссылке GET параметр `token` и будет токеном для присоединения.

        Args:
            user_id (:obj:`int`): Владелец плейлиста.
            token (:obj:`str`): Токен для присоединения.
            **kwargs: Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`bool`: :obj:`True` при успешном выполнении запроса, иначе :obj:`False`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/playlists/collective/join'

        params = {'uid': user_id, 'token': token}

        result = await self._request.post(url, params=params, **kwargs)

        return result == 'ok'

    @log
    async def users_playlists_list(self, user_id: UserIdType = None, *args: Any, **kwargs: Any) -> List[Playlist]:
        """Получение списка плейлистов пользователя.

        Args:
            user_id (:obj:`str` | :obj:`int`, optional): Уникальный идентификатор пользователя. Если не указан
                используется ID текущего пользователя.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`list` из :obj:`yandex_music.Playlist`: Плейлисты пользователя.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        if user_id is None and self.account_uid is not None:
            user_id = self.account_uid

        url = f'{self.base_url}/users/{user_id}/playlists/list'

        result = await self._request.get(url, *args, **kwargs)

        return list(Playlist.de_list(result, self))

    @log
    async def playlist(self, playlist_uuid: str, *args: Any, **kwargs: Any) -> Optional[Playlist]:
        """Получение плейлиста по его UUID.

        Args:
            playlist_uuid (:obj:`str`): UUID плейлиста.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.Playlist` | :obj:`None`: Плейлист или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/playlist/{playlist_uuid}'

        result = await self._request.get(url, *args, **kwargs)

        return Playlist.de_json(result, self)

    @log
    async def playlist_similar_entities(
        self, playlist_uuid: str, *args: Any, **kwargs: Any
    ) -> Optional[PlaylistSimilarEntities]:
        """Получение похожих сущностей для плейлиста.

        Args:
            playlist_uuid (:obj:`str`): UUID плейлиста.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.PlaylistSimilarEntities` | :obj:`None`: Похожие сущности или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/playlist/{playlist_uuid}/similar-entities'

        result = await self._request.get(url, *args, **kwargs)

        return PlaylistSimilarEntities.de_json(result, self)

    @log
    async def playlists(
        self, playlist_ids: Union[List[str], str], *args: Any, **kwargs: Any
    ) -> Optional[PlaylistsList]:
        """Получение списка плейлистов по идентификаторам.

        Note:
            Идентификаторы плейлистов имеют формат ``uid:kind`` (например, ``503646255:161344908``).

        Args:
            playlist_ids (:obj:`str` | :obj:`list` из :obj:`str`): Идентификатор плейлиста или список идентификаторов
                в формате ``uid:kind``.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.PlaylistsList` | :obj:`None`: Список плейлистов или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/playlists'

        if isinstance(playlist_ids, list):
            playlist_ids = ','.join(playlist_ids)

        kwargs['params'] = {'playlistIds': playlist_ids}
        result = await self._request.get(url, *args, **kwargs)

        return PlaylistsList.de_json(result, self)

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

    @log
    async def playlists_personal(self, playlist_id: str, *args: Any, **kwargs: Any) -> Optional[GeneratedPlaylist]:
        """Получение персонального плейлиста.

        Note:
            Известные значения ``playlist_id``: ``daily`` (Плейлист дня), ``missedLikes`` (Тайник),
            ``recentTracks`` (Премьера), ``neverHeard`` (Дежавю), ``podcasts`` (Подкасты недели),
            ``origin`` (Плейлист с Алисой).

        Args:
            playlist_id (:obj:`str`): Идентификатор персонального плейлиста.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.GeneratedPlaylist` | :obj:`None`: Персональный плейлист или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/playlists/personal/{playlist_id}'

        result = await self._request.get(url, *args, **kwargs)

        return GeneratedPlaylist.de_json(result, self)

    @log
    async def users_playlists_description(
        self,
        kind: Union[str, int],
        description: str,
        user_id: UserIdType = None,
        *args: Any,
        **kwargs: Any,
    ) -> Optional[Playlist]:
        """Изменение описания плейлиста.

        Args:
            kind (:obj:`str` | :obj:`int`): Уникальный идентификатор плейлиста.
            description (:obj:`str`): Новое описание.
            user_id (:obj:`str` | :obj:`int`, optional): Уникальный идентификатор пользователя владеющим плейлистом.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.Playlist` | :obj:`None`: Изменённый плейлист или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        if user_id is None and self.account_uid is not None:
            user_id = self.account_uid

        url = f'{self.base_url}/users/{user_id}/playlists/{kind}/description'

        result = await self._request.post(url, {'value': description}, *args, **kwargs)

        return Playlist.de_json(result, self)

    @log
    async def users_playlists_trailer(
        self,
        kind: Union[str, int],
        user_id: UserIdType = None,
        *args: Any,
        **kwargs: Any,
    ) -> Optional[PlaylistTrailer]:
        """Получение трейлера плейлиста.

        Args:
            kind (:obj:`str` | :obj:`int`): Уникальный идентификатор плейлиста.
            user_id (:obj:`str` | :obj:`int`, optional): Уникальный идентификатор пользователя владеющим плейлистом.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.PlaylistTrailer` | :obj:`None`: Трейлер плейлиста или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        if user_id is None and self.account_uid is not None:
            user_id = self.account_uid

        url = f'{self.base_url}/users/{user_id}/playlists/{kind}/trailer'

        result = await self._request.get(url, *args, **kwargs)

        return PlaylistTrailer.de_json(result, self)

    @log
    async def users_playlists_kinds(self, user_id: UserIdType = None, *args: Any, **kwargs: Any) -> List[int]:
        """Получение списка идентификаторов (kind) плейлистов пользователя.

        Args:
            user_id (:obj:`str` | :obj:`int`, optional): Уникальный идентификатор пользователя. Если не указан
                используется ID текущего пользователя.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`list` из :obj:`int`: Список идентификаторов плейлистов.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        if user_id is None and self.account_uid is not None:
            user_id = self.account_uid

        url = f'{self.base_url}/users/{user_id}/playlists/list/kinds'

        result = await self._request.get(url, *args, **kwargs)

        if isinstance(result, list):
            return result
        return []

    # camelCase псевдонимы

    #: Псевдоним для :attr:`users_settings`
    usersSettings = users_settings
    #: Псевдоним для :attr:`users_playlists`
    usersPlaylists = users_playlists
    #: Псевдоним для :attr:`users_playlists_recommendations`
    usersPlaylistsRecommendations = users_playlists_recommendations
    #: Псевдоним для :attr:`users_playlists_create`
    usersPlaylistsCreate = users_playlists_create
    #: Псевдоним для :attr:`users_playlists_delete`
    usersPlaylistsDelete = users_playlists_delete
    #: Псевдоним для :attr:`users_playlists_name`
    usersPlaylistsName = users_playlists_name
    #: Псевдоним для :attr:`users_playlists_visibility`
    usersPlaylistsVisibility = users_playlists_visibility
    #: Псевдоним для :attr:`users_playlists_change`
    usersPlaylistsChange = users_playlists_change
    #: Псевдоним для :attr:`users_playlists_insert_track`
    usersPlaylistsInsertTrack = users_playlists_insert_track
    #: Псевдоним для :attr:`users_playlists_delete_track`
    usersPlaylistsDeleteTrack = users_playlists_delete_track
    #: Псевдоним для :attr:`playlists_collective_join`
    playlistsCollectiveJoin = playlists_collective_join
    #: Псевдоним для :attr:`users_playlists_list`
    usersPlaylistsList = users_playlists_list
    #: Псевдоним для :attr:`playlist_similar_entities`
    playlistSimilarEntities = playlist_similar_entities
    #: Псевдоним для :attr:`playlists_list`
    playlistsList = playlists_list
    #: Псевдоним для :attr:`playlists_personal`
    playlistsPersonal = playlists_personal
    #: Псевдоним для :attr:`users_playlists_description`
    usersPlaylistsDescription = users_playlists_description
    #: Псевдоним для :attr:`users_playlists_trailer`
    usersPlaylistsTrailer = users_playlists_trailer
    #: Псевдоним для :attr:`users_playlists_kinds`
    usersPlaylistsKinds = users_playlists_kinds
