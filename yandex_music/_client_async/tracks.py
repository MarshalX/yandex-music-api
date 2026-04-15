from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

from yandex_music import (
    DownloadInfo,
    ShotEvent,
    SimilarTracks,
    Supplement,
    TrackFullInfo,
    TrackLyrics,
    TrackTrailer,
)
from yandex_music._client_async import log
from yandex_music._client_base import ClientBase, is_dict
from yandex_music.utils.sign_request import get_sign_request

if TYPE_CHECKING:
    from yandex_music.utils.request_async import Request


class TracksMixin(ClientBase):
    """Миксин для методов, связанных с треками."""

    _request: 'Request'

    @log
    async def tracks_download_info(
        self,
        track_id: Union[str, int],
        get_direct_links: bool = False,
        *args: Any,
        **kwargs: Any,
    ) -> List[DownloadInfo]:
        """Получение информации о доступных вариантах загрузки трека.

        Args:
            track_id (:obj:`str` | :obj:`list` из :obj:`str`): Уникальный идентификатор трека или треков.
            get_direct_links (:obj:`bool`, optional): Получить ли при вызове метода прямую ссылку на загрузку.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`list` из :obj:`yandex_music.DownloadInfo` | :obj:`None`: Варианты загрузки трека или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/tracks/{track_id}/download-info'

        result = await self._request.get(url, *args, **kwargs)

        return await DownloadInfo.de_list_async(result, self, get_direct_links)

    @log
    async def track_supplement(self, track_id: Union[str, int], *args: Any, **kwargs: Any) -> Optional[Supplement]:
        """Получение дополнительной информации о треке.

        Warning:
            Получение текста из дополнительной информации устарело. Используйте
            :func:`yandex_music.ClientAsync.tracks_lyrics`.

        Args:
            track_id (:obj:`str` | :obj:`int`): Уникальный идентификатор трека.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.Supplement`: Дополнительная информация о треке.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/tracks/{track_id}/supplement'

        result = await self._request.get(url, *args, **kwargs)

        return Supplement.de_json(result, self)

    @log
    async def tracks_lyrics(
        self,
        track_id: Union[str, int],
        format_: str = 'TEXT',
        **kwargs: Any,
    ) -> Optional[TrackLyrics]:
        """Получение текста трека.

        Note:
            Для работы с методом необходима авторизация.

            Известные значения для аргумента format:
                - `LRC` - формат с временными метками.
                - `TEXT` - простой текст.

        Args:
            track_id (:obj:`str` | :obj:`int`): Уникальный идентификатор трека.
            format_ (:obj:`str`): Формат текста.
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.TrackLyrics` | :obj:`None`: Информация о тексте трека.

        Raises:
            :class:`yandex_music.exceptions.UnauthorizedError`: Метод вызван без авторизации.
            :class:`yandex_music.exceptions.NotFoundError`: Текст у трека отсутствует.
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/tracks/{track_id}/lyrics'

        sign = get_sign_request(track_id)
        params = {
            'format': format_,
            'timeStamp': sign.timestamp,
            'sign': sign.value,
        }

        result = await self._request.get(url, params=params, **kwargs)

        return TrackLyrics.de_json(result, self)

    @log
    async def tracks_similar(self, track_id: Union[str, int], *args: Any, **kwargs: Any) -> Optional[SimilarTracks]:
        """Получение похожих треков.

        Args:
            track_id (:obj:`str` | :obj:`int`): Уникальный идентификатор трека.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.SimilarTracks`: Похожие треки на другой трек.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/tracks/{track_id}/similar'

        result = await self._request.get(url, *args, **kwargs)

        return SimilarTracks.de_json(result, self)

    @log
    async def play_audio(
        self,
        track_id: Union[str, int],
        from_: str,
        album_id: Union[str, int],
        playlist_id: Optional[str] = None,
        from_cache: bool = False,
        play_id: Optional[str] = None,
        uid: Optional[int] = None,
        timestamp: Optional[str] = None,
        track_length_seconds: int = 0,
        total_played_seconds: int = 0,
        end_position_seconds: int = 0,
        client_now: Optional[str] = None,
        *args: Any,
        **kwargs: Any,
    ) -> bool:
        """Метод для отправки текущего состояния прослушиваемого трека.

        Args:
            track_id (:obj:`str` | :obj:`int`): Уникальный идентификатор трека.
            from_ (:obj:`str`): Наименования клиента с которого происходит прослушивание.
            album_id (:obj:`str` | :obj:`int`): Уникальный идентификатор альбома.
            playlist_id (:obj:`str`, optional): Уникальный идентификатор плейлиста, если таковой прослушивается.
            from_cache (:obj:`bool`, optional): Проигрывается ли трек с кеша.
            play_id (:obj:`str`, optional): Уникальный идентификатор проигрывания.
            uid (:obj:`int`, optional): Уникальный идентификатор пользователя.
            timestamp (:obj:`str`, optional): Текущая дата и время в ISO.
            track_length_seconds (:obj:`int`, optional): Продолжительность трека в секундах.
            total_played_seconds (:obj:`int`, optional): Сколько было всего воспроизведено трека в секундах.
            end_position_seconds (:obj:`int`, optional): Окончательное значение воспроизведенных секунд.
            client_now (:obj:`str`, optional): Текущая дата и время клиента в ISO.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`bool`: :obj:`True` при успешном выполнении запроса, иначе :obj:`False`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        if uid is None and self.account_uid is not None:
            uid = self.account_uid

        url = f'{self.base_url}/play-audio'

        data = {
            'track-id': track_id,
            'from-cache': str(from_cache),
            'from': from_,
            'play-id': play_id or '',
            'uid': uid,
            'timestamp': timestamp or f'{datetime.now().isoformat()}Z',
            'track-length-seconds': track_length_seconds,
            'total-played-seconds': total_played_seconds,
            'end-position-seconds': end_position_seconds,
            'album-id': album_id,
            'playlist-id': playlist_id,
            'client-now': client_now or f'{datetime.now().isoformat()}Z',
        }

        result = await self._request.post(url, data, *args, **kwargs)

        return result == 'ok'

    @log
    async def after_track(
        self,
        next_track_id: Union[str, int],
        context_item: str,
        prev_track_id: Optional[Union[str, int]] = None,
        context: str = 'playlist',
        types: str = 'shot',
        from_: str = 'mobile-landing-origin-default',
        *args: Any,
        **kwargs: Any,
    ) -> Optional[ShotEvent]:
        """Получение рекламы или шота от Алисы после трека.

        Note:
            При получения шота от Алисы `prev_track_id` можно не указывать.

            Если `context = 'playlist'`, то в `context_item` необходимо передать `{OWNER_PLAYLIST}:{ID_PLAYLIST}`.
            Плейлист с Алисой имеет владельца с `id = 940441070`.

            ID плейлиста можно получить из блоков landing'a. Получить шот чужого плейлиста нельзя.

            Известные значения `context`: `playlist`.

            Известные значения `types`: `shot`, `ad`.

        Args:
            prev_track_id (:obj:`str` | :obj:`int`): Уникальный идентификатор предыдущего трека.
            next_track_id (:obj:`str` | :obj:`int`): Уникальный идентификатор следующего трека.
            context_item (:obj:`str`): Уникальный идентификатор контекста.
            context (:obj:`str`, optional): Место, откуда было вызвано получение.
            types (:obj:`str`, optional): Тип того, что вернуть после трека.
            from_ (:obj:`str`, optional): Место, с которого попали в контекст.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.ShotEvent`: Шот от Алисы или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/after-track'

        params = {
            'from': from_,
            'prevTrackId': prev_track_id,
            'nextTrackId': next_track_id,
            'context': context,
            'contextItem': context_item,
            'types': types,
        }

        result = await self._request.get(url, params, *args, **kwargs)

        # TODO (MarshalX) судя по всему ручка ещё возвращает рекламу после треков для пользователей без подписки.
        #  https://github.com/MarshalX/yandex-music-api/issues/557
        if is_dict(result):
            return ShotEvent.de_json(result.get('shotEvent'), self)
        return None

    @log
    async def tracks_trailer(self, track_id: Union[str, int], *args: Any, **kwargs: Any) -> Optional[TrackTrailer]:
        """Получение трейлера трека.

        Args:
            track_id (:obj:`str` | :obj:`int`): Уникальный идентификатор трека.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.TrackTrailer` | :obj:`None`: Трейлер трека или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/tracks/{track_id}/trailer'

        result = await self._request.get(url, *args, **kwargs)

        return TrackTrailer.de_json(result, self)

    @log
    async def tracks_full_info(self, track_id: Union[str, int], *args: Any, **kwargs: Any) -> Optional[TrackFullInfo]:
        """Получение полной информации о треке.

        Args:
            track_id (:obj:`str` | :obj:`int`): Уникальный идентификатор трека.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.TrackFullInfo` | :obj:`None`: Полная информация о треке или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/tracks/{track_id}/full-info'

        result = await self._request.get(url, *args, **kwargs)

        return TrackFullInfo.de_json(result, self)

    # camelCase псевдонимы

    #: Псевдоним для :attr:`tracks_download_info`
    tracksDownloadInfo = tracks_download_info
    #: Псевдоним для :attr:`track_supplement`
    trackSupplement = track_supplement
    #: Псевдоним для :attr:`tracks_lyrics`
    tracksLyrics = tracks_lyrics
    #: Псевдоним для :attr:`tracks_similar`
    tracksSimilar = tracks_similar
    #: Псевдоним для :attr:`play_audio`
    playAudio = play_audio
    #: Псевдоним для :attr:`after_track`
    afterTrack = after_track
    #: Псевдоним для :attr:`tracks_trailer`
    tracksTrailer = tracks_trailer
    #: Псевдоним для :attr:`tracks_full_info`
    tracksFullInfo = tracks_full_info
