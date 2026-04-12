from typing import TYPE_CHECKING, Any, List, Optional, Union

from yandex_music import Like, TracksList
from yandex_music._client_async import log
from yandex_music._client_base import ClientBase, UserIdType

if TYPE_CHECKING:
    from yandex_music.base import JSONType
    from yandex_music.utils.request_async import Request


class LikesMixin(ClientBase):
    """Миксин для методов, связанных с лайками и дизлайками."""

    _request: 'Request'

    async def _like_action(
        self,
        object_type: str,
        ids: Union[List[Union[str, int]], str, int],
        remove: bool = False,
        user_id: UserIdType = None,
        *args: Any,
        **kwargs: Any,
    ) -> bool:
        """Действия с отметкой "Мне нравится".

        Note:
            Типы объектов: `track` - трек, `artist` - исполнитель, `playlist` - плейлист, `album` - альбом.

            Идентификатор плейлиста указывается в формате `owner_id:playlist_id`. Где `playlist_id` - идентификатор
            плейлиста, `owner_id` - уникальный идентификатор владельца плейлиста.

        Args:
            object_type (:obj:`str`): Тип объекта.
            ids (:obj:`str` | :obj:`int` | :obj:`list` из :obj:`str` | :obj:`list` из :obj:`int`): Уникальный
                идентификатор объекта или объектов.
            remove (:obj:`bool`, optional): Если :obj:`True` то снимает отметку, иначе ставит.
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

        action = 'remove' if remove else 'add-multiple'
        url = f'{self.base_url}/users/{user_id}/likes/{object_type}s/{action}'

        result = await self._request.post(url, {f'{object_type}-ids': ids}, *args, **kwargs)

        if object_type == 'track':
            return 'revision' in result

        return result == 'ok'

    @log
    async def users_likes_tracks_add(
        self,
        track_ids: Union[List[Union[str, int]], str, int],
        user_id: UserIdType = None,
        **kwargs: Any,
    ) -> bool:
        """Поставить отметку "Мне нравится" треку/трекам.

        Note:
            Так же снимает отметку "Не рекомендовать" если она есть.

        Args:
            track_ids (:obj:`str` | :obj:`int` | :obj:`list` из :obj:`str` | :obj:`list` из :obj:`int`): Уникальный
                идентификатор трека или треков.
            user_id (:obj:`str` | :obj:`int`, optional): Уникальный идентификатор пользователя. Если не указан
                используется ID текущего пользователя.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`bool`: :obj:`True` при успешном выполнении запроса, иначе :obj:`False`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        return await self._like_action('track', track_ids, remove=False, user_id=user_id, **kwargs)

    @log
    async def users_likes_tracks_remove(
        self,
        track_ids: Union[List[Union[str, int]], str, int],
        user_id: UserIdType = None,
        **kwargs: Any,
    ) -> bool:
        """Снять отметку "Мне нравится" у трека/треков.

        Args:
            track_ids (:obj:`str` | :obj:`int` | :obj:`list` из :obj:`str` | :obj:`list` из :obj:`int`): Уникальный
                идентификатор трека или треков.
            user_id (:obj:`str` | :obj:`int`, optional): Уникальный идентификатор пользователя. Если не указан
                используется ID текущего пользователя.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`bool`: :obj:`True` при успешном выполнении запроса, иначе :obj:`False`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        return await self._like_action('track', track_ids, remove=True, user_id=user_id, **kwargs)

    @log
    async def users_likes_artists_add(
        self,
        artist_ids: Union[List[Union[str, int]], str, int],
        user_id: UserIdType = None,
        **kwargs: Any,
    ) -> bool:
        """Поставить отметку "Мне нравится" исполнителю/исполнителям.

        Args:
            artist_ids (:obj:`str` | :obj:`int` | :obj:`list` из :obj:`str` | :obj:`list` из :obj:`int`): Уникальный
                идентификатор артиста или артистов.
            user_id (:obj:`str` | :obj:`int`, optional): Уникальный идентификатор пользователя. Если не указан
                используется ID текущего пользователя.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`bool`: :obj:`True` при успешном выполнении запроса, иначе :obj:`False`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        return await self._like_action('artist', artist_ids, remove=False, user_id=user_id, **kwargs)

    @log
    async def users_likes_artists_remove(
        self,
        artist_ids: Union[List[Union[str, int]], str, int],
        user_id: UserIdType = None,
        **kwargs: Any,
    ) -> bool:
        """Снять отметку "Мне нравится" у исполнителя/исполнителей.

        Args:
            artist_ids (:obj:`str` | :obj:`int` | :obj:`list` из :obj:`str` | :obj:`list` из :obj:`int`): Уникальный
                идентификатор артиста или артистов.
            user_id (:obj:`str` | :obj:`int`, optional): Уникальный идентификатор пользователя. Если не указан
                используется ID текущего пользователя.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`bool`: :obj:`True` при успешном выполнении запроса, иначе :obj:`False`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        return await self._like_action('artist', artist_ids, remove=True, user_id=user_id, **kwargs)

    @log
    async def users_likes_playlists_add(
        self,
        playlist_ids: Union[List[Union[str, int]], str, int],
        user_id: UserIdType = None,
        **kwargs: Any,
    ) -> bool:
        """Поставить отметку "Мне нравится" плейлисту/плейлистам.

        Note:
            Идентификатор плейлиста указывается в формате `owner_id:playlist_id`. Где `playlist_id` - идентификатор
            плейлиста, `owner_id` - уникальный идентификатор владельца плейлиста.

        Args:
            playlist_ids (:obj:`str` | :obj:`int` | :obj:`list` из :obj:`str` | :obj:`list` из :obj:`int`): Уникальный
                идентификатор плейлиста или плейлистов.
            user_id (:obj:`str` | :obj:`int`, optional): Уникальный идентификатор пользователя. Если не указан
                используется ID текущего пользователя.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`bool`: :obj:`True` при успешном выполнении запроса, иначе :obj:`False`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        return await self._like_action('playlist', playlist_ids, remove=False, user_id=user_id, **kwargs)

    @log
    async def users_likes_playlists_remove(
        self,
        playlist_ids: Union[List[Union[str, int]], str, int],
        user_id: UserIdType = None,
        **kwargs: Any,
    ) -> bool:
        """Снять отметку "Мне нравится" у плейлиста/плейлистов.

        Note:
            Идентификатор плейлиста указывается в формате `owner_id:playlist_id`. Где `playlist_id` - идентификатор
            плейлиста, `owner_id` - уникальный идентификатор владельца плейлиста.

        Args:
            playlist_ids (:obj:`str` | :obj:`int` | :obj:`list` из :obj:`str` | :obj:`list` из :obj:`int`): Уникальный
                идентификатор плейлиста или плейлистов.
            user_id (:obj:`str` | :obj:`int`, optional): Уникальный идентификатор пользователя. Если не указан
                используется ID текущего пользователя.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`bool`: :obj:`True` при успешном выполнении запроса, иначе :obj:`False`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        return await self._like_action('playlist', playlist_ids, remove=True, user_id=user_id, **kwargs)

    @log
    async def users_likes_albums_add(
        self,
        album_ids: Union[List[Union[str, int]], str, int],
        user_id: UserIdType = None,
        **kwargs: Any,
    ) -> bool:
        """Поставить отметку "Мне нравится" альбому/альбомам.

        Args:
            album_ids (:obj:`str` | :obj:`int` | :obj:`list` из :obj:`str` | :obj:`list` из :obj:`int`): Уникальный
                идентификатор артиста или артистов.
            user_id (:obj:`str` | :obj:`int`, optional): Уникальный идентификатор пользователя. Если не указан
                используется ID текущего пользователя.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`bool`: :obj:`True` при успешном выполнении запроса, иначе :obj:`False`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        return await self._like_action('album', album_ids, remove=False, user_id=user_id, **kwargs)

    @log
    async def users_likes_albums_remove(
        self,
        album_ids: Union[List[Union[str, int]], str, int],
        user_id: UserIdType = None,
        **kwargs: Any,
    ) -> bool:
        """Снять отметку "Мне нравится" у альбома/альбомов.

        Args:
            album_ids (:obj:`str` | :obj:`int` | :obj:`list` из :obj:`str` | :obj:`list` из :obj:`int`): Уникальный
                идентификатор артиста или артистов.
            user_id (:obj:`str` | :obj:`int`, optional): Уникальный идентификатор пользователя. Если не указан
                используется ID текущего пользователя.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`bool`: :obj:`True` при успешном выполнении запроса, иначе :obj:`False`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        return await self._like_action('album', album_ids, remove=True, user_id=user_id, **kwargs)

    async def _get_likes(
        self,
        object_type: str,
        user_id: UserIdType = None,
        params: Optional['JSONType'] = None,
        *args: Any,
        **kwargs: Any,
    ) -> Union[List[Like], Optional[TracksList]]:
        """Получение объектов с отметкой "Мне нравится".

        Args:
            object_type (:obj:`str`): Тип объекта.
            user_id (:obj:`str` | :obj:`int`, optional): Уникальный идентификатор пользователя. Если не указан
                используется ID текущего пользователя.
            params (:obj:`dict`, optional): Параметры, которые будут переданы в запрос.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`list` из :obj:`yandex_music.Like` | :obj:`yandex_music.TracksList`: Объекты с отметкой "Мне нравится".

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        if user_id is None and self.account_uid is not None:
            user_id = self.account_uid

        url = f'{self.base_url}/users/{user_id}/likes/{object_type}s'

        result = await self._request.get(url, params, *args, **kwargs)

        if object_type == 'track':
            return TracksList.de_json(result.get('library'), self)

        return Like.de_list(result, self, object_type)

    @log
    async def users_likes_tracks(
        self,
        user_id: UserIdType = None,
        if_modified_since_revision: int = 0,
        *args: Any,
        **kwargs: Any,
    ) -> Optional[TracksList]:
        """Получение треков с отметкой "Мне нравится".

        Args:
            user_id (:obj:`str` | :obj:`int`, optional): Уникальный идентификатор пользователя. Если не указан
                используется ID текущего пользователя.
            if_modified_since_revision (:obj:`int`, optional): TODO.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.TracksList`: Треки с отметкой "Мне нравится".

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        return await self._get_likes(
            'track', user_id, {'if-modified-since-revision': if_modified_since_revision}, *args, **kwargs
        )

    @log
    async def users_likes_albums(
        self, user_id: UserIdType = None, rich: bool = True, *args: Any, **kwargs: Any
    ) -> List[Like]:
        """Получение альбомов с отметкой "Мне нравится".

        Args:
            user_id (:obj:`str` | :obj:`int`, optional): Уникальный идентификатор пользователя. Если не указан
                используется ID текущего пользователя.
            rich (:obj:`bool`, optional): Если False, то приходит укороченная версия.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`list` из :obj:`yandex_music.Like`: Альбомы с отметкой "Мне нравится".

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        return await self._get_likes('album', user_id, {'rich': str(rich)}, *args, **kwargs)

    @log
    async def users_likes_artists(
        self,
        user_id: UserIdType = None,
        with_timestamps: bool = True,
        *args: Any,
        **kwargs: Any,
    ) -> List[Like]:
        """Получение артистов с отметкой "Мне нравится".

        Args:
            user_id (:obj:`str` | :obj:`int`, optional): Уникальный идентификатор пользователя. Если не указан
                используется ID текущего пользователя.
            with_timestamps (:obj:`bool`, optional):  С временными метками TODO.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`list` из :obj:`yandex_music.Like`: Артисты с отметкой "Мне нравится".

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        return await self._get_likes('artist', user_id, {'with-timestamps': str(with_timestamps)}, *args, **kwargs)

    @log
    async def users_likes_playlists(self, user_id: UserIdType = None, *args: Any, **kwargs: Any) -> List[Like]:
        """Получение плейлистов с отметкой "Мне нравится".

        Args:
            user_id (:obj:`str` | :obj:`int`, optional): Уникальный идентификатор пользователя. Если не указан
                используется ID текущего пользователя.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`list` из :obj:`yandex_music.Like`: Плейлисты с отметкой "Мне нравится".

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        return await self._get_likes('playlist', user_id, *args, **kwargs)

    @log
    async def users_dislikes_tracks(
        self,
        user_id: UserIdType = None,
        if_modified_since_revision: int = 0,
        *args: Any,
        **kwargs: Any,
    ) -> Optional[TracksList]:
        """Получение треков с отметкой "Не рекомендовать".

        Args:
            user_id (:obj:`str` | :obj:`int`, optional): Уникальный идентификатор пользователя. Если не указан
                используется ID текущего пользователя.
            if_modified_since_revision (:obj:`bool`, optional): TODO.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`list` из :obj:`yandex_music.TracksList`: Треки с отметкой "Не рекомендовать".

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        if user_id is None and self.account_uid is not None:
            user_id = self.account_uid

        url = f'{self.base_url}/users/{user_id}/dislikes/tracks'

        result = await self._request.get(
            url, {'if_modified_since_revision': if_modified_since_revision}, *args, **kwargs
        )

        return TracksList.de_json(result.get('library'), self)

    async def _dislike_action(
        self,
        ids: Union[List[Union[str, int]], str, int],
        remove: bool = False,
        user_id: UserIdType = None,
        *args: Any,
        **kwargs: Any,
    ) -> bool:
        """Действия с отметкой "Не рекомендовать".

        Args:
            ids (:obj:`str` | :obj:`int` | :obj:`list` из :obj:`str` | :obj:`list` из :obj:`int`): Уникальный
                идентификатор объекта или объектов.
            remove (:obj:`bool`, optional): Если :obj:`True`, то снимает отметку, иначе ставит.
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

        action = 'remove' if remove else 'add-multiple'
        url = f'{self.base_url}/users/{user_id}/dislikes/tracks/{action}'

        result = await self._request.post(url, {'track-ids': ids}, *args, **kwargs)

        return 'revision' in result

    @log
    async def users_dislikes_tracks_add(
        self,
        track_ids: Union[List[Union[str, int]], str, int],
        user_id: UserIdType = None,
        **kwargs: Any,
    ) -> bool:
        """Поставить отметку "Не рекомендовать" треку/трекам.

        Note:
            Так же снимает отметку "Мне нравится" если она есть.

        Args:
            track_ids (:obj:`str` | :obj:`int` | :obj:`list` из :obj:`str` | :obj:`list` из :obj:`int`): Уникальный
                идентификатор трека или треков.
            user_id (:obj:`str` | :obj:`int`, optional): Уникальный идентификатор пользователя. Если не указан
                используется ID текущего пользователя.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`bool`: :obj:`True` при успешном выполнении запроса, иначе :obj:`False`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        return await self._dislike_action(track_ids, remove=False, user_id=user_id, **kwargs)

    @log
    async def users_dislikes_tracks_remove(
        self,
        track_ids: Union[List[Union[str, int]], str, int],
        user_id: UserIdType = None,
        **kwargs: Any,
    ) -> bool:
        """Снять отметку "Не рекомендовать" у трека/треков.

        Args:
            track_ids (:obj:`str` | :obj:`int` | :obj:`list` из :obj:`str` | :obj:`list` из :obj:`int`): Уникальный
                идентификатор трека или треков.
            user_id (:obj:`str` | :obj:`int`, optional): Уникальный идентификатор пользователя. Если не указан
                используется ID текущего пользователя.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`bool`: :obj:`True` при успешном выполнении запроса, иначе :obj:`False`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        return await self._dislike_action(track_ids, remove=True, user_id=user_id, **kwargs)

    # camelCase псевдонимы

    #: Псевдоним для :attr:`users_likes_tracks_add`
    usersLikesTracksAdd = users_likes_tracks_add
    #: Псевдоним для :attr:`users_likes_tracks_remove`
    usersLikesTracksRemove = users_likes_tracks_remove
    #: Псевдоним для :attr:`users_likes_artists_add`
    usersLikesArtistsAdd = users_likes_artists_add
    #: Псевдоним для :attr:`users_likes_artists_remove`
    usersLikesArtistsRemove = users_likes_artists_remove
    #: Псевдоним для :attr:`users_likes_playlists_add`
    usersLikesPlaylistsAdd = users_likes_playlists_add
    #: Псевдоним для :attr:`users_likes_playlists_remove`
    usersLikesPlaylistsRemove = users_likes_playlists_remove
    #: Псевдоним для :attr:`users_likes_albums_add`
    usersLikesAlbumsAdd = users_likes_albums_add
    #: Псевдоним для :attr:`users_likes_albums_remove`
    usersLikesAlbumsRemove = users_likes_albums_remove
    #: Псевдоним для :attr:`users_likes_tracks`
    usersLikesTracks = users_likes_tracks
    #: Псевдоним для :attr:`users_likes_albums`
    usersLikesAlbums = users_likes_albums
    #: Псевдоним для :attr:`users_likes_artists`
    usersLikesArtists = users_likes_artists
    #: Псевдоним для :attr:`users_likes_playlists`
    usersLikesPlaylists = users_likes_playlists
    #: Псевдоним для :attr:`users_dislikes_tracks`
    usersDislikesTracks = users_dislikes_tracks
    #: Псевдоним для :attr:`users_dislikes_tracks_add`
    usersDislikesTracksAdd = users_dislikes_tracks_add
    #: Псевдоним для :attr:`users_dislikes_tracks_remove`
    usersDislikesTracksRemove = users_dislikes_tracks_remove
