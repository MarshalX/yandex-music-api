import logging
from datetime import datetime

from yandex_music import YandexMusicObject, Status, Settings, PermissionAlerts, Experiments, Artist, Album, Playlist, \
    TracksList, Track, AlbumsLikes, ArtistsLikes, PlaylistsLikes, Feed, PromoCodeStatus, DownloadInfo, Search, \
    Suggestions, Landing, Genre, Dashboard, StationResult, StationTracksResult
from yandex_music.utils.request import Request
from yandex_music.utils.difference import Difference
from yandex_music.exceptions import InvalidToken

CLIENT_ID = '23cabbbdc6cd418abb4b39c32c41195d'
CLIENT_SECRET = '53bc75238f0c4d08a118e51fe9203300'

de_list = {
    'artist': Artist.de_list,
    'album': Album.de_list,
    'track': Track.de_list,
    'playlist': Playlist.de_list,
}

de_list_likes = {
    'artist': ArtistsLikes.de_list,
    'album': AlbumsLikes.de_list,
    'playlist': PlaylistsLikes.de_list,
}


class Client(YandexMusicObject):
    """Класс представляющий клиент Yandex Music.

    Attributes:
        logger (:obj:`logging.Logger`): Объект логера.
        token (:obj:`str`): Уникальный ключ для аутентификации.
        base_url (:obj:`str`): Ссылка на API Yandex Music.
        oauth_url (:obj:`str`): Ссылка на OAuth Yandex Music.
        account (:obj:`yandex_music.Account`): Объект класса :class:`yandex_music.Account` предоставляющего основную
            информацию об аккаунте.

    Args:
        username (:obj:`str`): Логин клиента (идентификатор).
        password (:obj:`str`): Пароль клиента (аутентификатор).
        token (:obj:`str`, optional): Уникальный ключ для аутентификации.
        base_url (:obj:`str`, optional): Ссылка на API Yandex Music.
        oauth_url (:obj:`str`, optional): Ссылка на OAuth Yandex Music.
        request (:obj:`yandex_music.utils.request.Request`, optional): Пре-инициализация
            :class:`yandex_music.utils.request.Request`.
    """

    def __init__(self, username, password, token=None, base_url=None, oauth_url=None, request=None):
        self.logger = logging.getLogger(__name__)
        self.token = token

        if base_url is None:
            base_url = 'https://api.music.yandex.net'
        if oauth_url is None:
            oauth_url = 'https://oauth.yandex.ru'

        self.base_url = base_url
        self.oauth_url = oauth_url

        self._request = request or Request(self)

        if self.token is None:
            self.token = self.generate_token_by_username_and_password(username, password)
            self.request.set_authorization(self.token)

        self.account = self.account_status().account

    @classmethod
    def from_token(cls, token):
        """Сокращение для авторизации по токену.

        Args:
            token (:obj:`str`, optional): Уникальный ключ для аутентификации.

        Returns:
            :obj:`yandex_music.Client`.
        """

        return cls(username=None, password=None, token=token)

    def generate_token_by_username_and_password(self, username, password, grant_type='password',
                                                timeout=None, *args, **kwargs):
        """Метод получения OAuth токена по логину и паролю.

        Args:
            username (:obj:`str`): Логин клиента (идентификатор).
            password (:obj:`str`): Пароль клиента (аутентификатор).
            grant_type (:obj:`str`, optional): Тип разрешения OAuth.
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`str`: OAuth токен.

        Raises:
            :class:`yandex_music.YandexMusicError`
        """

        url = f'{self.oauth_url}/token'

        data = {
            'grant_type': grant_type,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'username': username,
            'password': password
        }

        result = self._request.post(url, data, timeout=timeout, *args, **kwargs)

        return result.get('access_token')

    @staticmethod
    def _validate_token(token: str):
        """Примитивная валидация токена.

        Args:
            token (:obj:`str`): токен для проверки

        Returns:
            :obj:`str`: Токен.

        Raises:
            :class:`yandex_music.exceptions.InvalidToken`: Если токен недействителен.
        """

        if any(x.isspace() for x in token):
            raise InvalidToken()

        if len(token) != 39:
            raise InvalidToken()

        return token

    @property
    def request(self):
        """:obj:`yandex_music.utils.request.Request`: Объект вспомогательного класса для отправки запросов."""
        return self._request

    def account_status(self, timeout=None, *args, **kwargs):
        """Получение статуса аккаунта. Нет обязательных параметров.

        Args:
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.Status`: Объекта класса :class:`yandex_music.Status` предоставляющий информацию об
            аккаунте если валиден, иначе :obj:`None`.

        Raises:
            :class:`yandex_music.YandexMusicError`
        """

        url = f'{self.base_url}/account/status'

        result = self._request.get(url, timeout=timeout, *args, **kwargs)

        return Status.de_json(result, self)

    def settings(self, timeout=None, *args, **kwargs):
        """Получение предложений по покупке. Нет обязательных параметров.

        Args:
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.Settings`: Объекта класса :class:`yandex_music.Settings` предоставляющий информацию о
            предлагаемых продуктах, иначе :obj:`None`.

        Raises:
            :class:`yandex_music.YandexMusicError`
        """

        url = f'{self.base_url}/settings'

        result = self._request.get(url, timeout=timeout, *args, **kwargs)

        return Settings.de_json(result, self)

    def permission_alerts(self, timeout=None, *args, **kwargs):
        """Получение оповещений. Нет обязательных параметров.

        Args:
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.PermissionAlerts`: Объекта класса :class:`yandex_music.PermissionAlerts`
            представляющий оповещения, иначе :obj:`None`.

        Raises:
            :class:`yandex_music.YandexMusicError`
        """

        url = f'{self.base_url}/permission-alerts'

        result = self._request.get(url, timeout=timeout, *args, **kwargs)

        return PermissionAlerts.de_json(result, self)

    def account_experiments(self, timeout=None, *args, **kwargs):
        """Получение значений экспериментальных функций аккаунта.

        Args:
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.Experiments`: Объекта класса :class:`yandex_music.Experiments`
            представляющий состояния экспериментальных функций, иначе :obj:`None`.

        Raises:
            :class:`yandex_music.YandexMusicError`
        """

        url = f'{self.base_url}/account/experiments'

        result = self._request.get(url, timeout=timeout, *args, **kwargs)

        return Experiments.de_json(result, self)

    def consume_promo_code(self, code: str, language: str = 'en', timeout=None, *args, **kwargs):
        """Активация промо-кода.

        Args:
            code (:obj:`str`): Промо-код.
            language (:obj:`str`, optional): Язык ответа API в ISO 639-1.
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.PromoCodeStatus`: Объекта класса :class:`yandex_music.PromoCodeStatus`
            представляющий информацию об активации промо-кода, иначе :obj:`None`.

        Raises:
            :class:`yandex_music.YandexMusicError`
        """

        url = f'{self.base_url}/account/consume-promo-code'

        result = self._request.post(url, {'code': code, 'language': language}, timeout=timeout, *args, **kwargs)

        return PromoCodeStatus.de_json(result, self)

    def feed(self, timeout=None, *args, **kwargs):
        """Получение потока информации (фида) подобранного под пользователя. Содержит умные плейлисты.

        Args:
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.Feed`: Объекта класса :class:`yandex_music.Feed`
            представляющий умные плейлисты пользователя, иначе :obj:`None`.

        Raises:
            :class:`yandex_music.YandexMusicError`
        """

        url = f'{self.base_url}/feed'

        result = self._request.get(url, timeout=timeout, *args, **kwargs)

        return Feed.de_json(result, self)

    def feed_wizard_is_passed(self, timeout=None, *args, **kwargs):
        url = f'{self.base_url}/feed/wizard/is-passed'

        result = self._request.get(url, timeout=timeout, *args, **kwargs)

        return result.get('is_wizard_passed') or False

    def landing(self, blocks: str or list, timeout=None, *args, **kwargs):
        """Получение лендинг-страницы содержащий блоки с новыми релизами, чартами, плейлистами с новинками и т.д.

        Поддерживаемые типы блоков: personalplaylists, promotions, new-releases, new-playlists, mixes,c hart, artists,
        albums, playlists, play_contexts.

        Args:
            blocks (:obj:`str` | :obj:`list` из :obj:`str`): Блок или список блоков необходимых для выдачи.
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.Landing`: Объекта класса :class:`yandex_music.Landing`
            представляющий лендинг-страницу, иначе :obj:`None`.

        Raises:
            :class:`yandex_music.YandexMusicError`
        """

        url = f'{self.base_url}/landing3'

        result = self._request.get(url, {'blocks': blocks}, timeout=timeout, *args, **kwargs)

        return Landing.de_json(result, self)

    def genres(self, timeout=None, *args, **kwargs):
        """Получение жанров музыки.

        Args:
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`list` из :obj:`yandex_music.Genre`: Список объектов класса :class:`yandex_music.Genre`
            представляющих жанры музыки, иначе :obj:`None`.

        Raises:
            :class:`yandex_music.YandexMusicError`
        """

        url = f'{self.base_url}/genres'

        result = self._request.get(url, timeout=timeout, *args, **kwargs)

        return Genre.de_list(result, self)

    def tracks_download_info(self, track_id: str or int, get_direct_links: bool = False, timeout=None, *args, **kwargs):
        """Получение информации о доступных вариантах загрузки трека.

        Args:
            track_id (:obj:`str` | :obj:`list` из :obj:`str`): Уникальный идентификатор трека или треков.
            get_direct_links (:obj:`bool`, optional): Получить ли при вызове метода прямую ссылку на загрузку.
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`list` из :obj:`yandex_music.DownloadInfo`: Список объектов класса :class:`yandex_music.DownloadInfo`
            представляющих варианты загрузки трека, иначе :obj:`None`.

        Raises:
            :class:`yandex_music.YandexMusicError`
        """

        url = f'{self.base_url}/tracks/{track_id}/download-info'

        result = self._request.get(url, timeout=timeout, *args, **kwargs)

        return DownloadInfo.de_list(result, self, get_direct_links)

    def play_audio(self,
                   track_id: str or int,
                   from_: str,
                   album_id: str or int,
                   playlist_id: str = None,
                   from_cache: bool = False,
                   play_id: str = None,
                   uid: int = None,
                   timestamp: str = None,
                   track_length_seconds: int = 0,
                   total_played_seconds: int = 0,
                   end_position_seconds: int = 0,
                   client_now: str = None,
                   timeout=None,
                   *args, **kwargs):
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
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`bool`: :obj:`True` при успешном выполнении запроса, иначе :obj:`False`.

        Raises:
            :class:`yandex_music.YandexMusicError`
        """

        url = f'{self.base_url}/play-audio'

        data = {
            'track-id': track_id,
            'from-cache': from_cache,
            'from': from_,
            'play-id': play_id or '',
            'uid': uid or self.account.uid,
            'timestamp': timestamp or f'{datetime.now().isoformat()}Z',
            'track-length-seconds': track_length_seconds,
            'total-played-seconds': total_played_seconds,
            'end-position-seconds': end_position_seconds,
            'album-id': album_id,
            'playlist-id': playlist_id,
            'client-now': client_now or f'{datetime.now().isoformat()}Z'
        }

        result = self._request.post(url, data, timeout=timeout, *args, **kwargs)

        return result == 'ok'

    def search(self,
               text: str,
               nocorrect: bool = False,
               type_: str = 'all',
               page: int = 0,
               playlist_in_best: bool = True,
               timeout=None,
               *args, **kwargs):
        """Осуществление поиска по запросу и типу, получение результатов. 

        Args:
            text (:obj:`str`): Текст запроса.
            nocorrect (:obj:`bool`): Без исправлений ли TODO.
            type_ (:obj:`str`): Среди какого типа искать (трек, плейлист, альбом, исполнитель).
            page (:obj:`int`): Номер страницы.
            playlist_in_best (:obj:`bool`): Выдавать ли плейлисты лучшим вариантом поиска.
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.Search`: Объекта класса :class:`yandex_music.Search`
            представляющий результаты поиска, иначе :obj:`None`.

        Raises:
            :class:`yandex_music.YandexMusicError`
        """

        url = f'{self.base_url}/search'

        params = {
            'text': text,
            'nocorrect': nocorrect,
            'type': type_,
            'page': page,
            'playlist-in-best': playlist_in_best,
        }

        result = self._request.get(url, params, timeout=timeout, *args, **kwargs)

        return Search.de_json(result, self)

    def search_suggest(self, part: str, timeout=None, *args, **kwargs):
        """Получение подсказок по введенной части поискового запроса.

        Args:
            part (:obj:`str`): Часть поискового запроса.
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.Suggestions`: Объекта класса :class:`yandex_music.Suggestions`
            представляющий подсказки для запроса, иначе :obj:`None`.

        Raises:
            :class:`yandex_music.YandexMusicError`
        """

        url = f'{self.base_url}/search/suggest'

        result = self._request.get(url, {'part': part}, timeout=timeout, *args, **kwargs)

        return Suggestions.de_json(result, self)

    def users_playlists(self, kind: str or int or list, user_id: str = None, timeout=None, *args, **kwargs):
        """Получение плейлиста или списка плейлистов по уникальным идентификаторам.

        Args:
            kind (:obj:`str` | :obj:`int` | :obj:`list` из :obj:`str` | :obj:`int`): Уникальный идентификатор плейлиста
                или их список.
            user_id: (:obj:`int`, optional): Уникальный идентификатор пользователя владеющим плейлистом.
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`list` из :obj:`yandex_music.Playlist`: Список объектов класса :class:`yandex_music.Playlist`
            представляющих плейлист, иначе :obj:`None`.

        Raises:
            :class:`yandex_music.YandexMusicError`
        """

        if user_id is None:
            user_id = self.account.uid

        url = f'{self.base_url}/users/{user_id}/playlists'

        data = {
            'kinds': kind
        }

        result = self._request.post(url, data, timeout=timeout, *args, **kwargs)

        return Playlist.de_list(result, self)

    def users_playlists_create(self, title: str, visibility: str = 'public', user_id: str = None,
                               timeout=None, *args, **kwargs):
        """Создание плейлиста.

        Args:
            title (:obj:`str`): Название.
            visibility (:obj:`str`, optional): Модификатор доступа.
            user_id: (:obj:`int`, optional): Уникальный идентификатор пользователя владеющим плейлистом.
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.Playlist`: Объекта класса :class:`yandex_music.Playlist`
            представляющий созданный плейлист, иначе :obj:`None`.

        Raises:
            :class:`yandex_music.YandexMusicError`
        """

        if user_id is None:
            user_id = self.account.uid

        url = f'{self.base_url}/users/{user_id}/playlists/create'

        data = {
            'title': title,
            'visibility': visibility
        }

        result = self._request.post(url, data, timeout=timeout, *args, **kwargs)

        return Playlist.de_json(result, self)

    def users_playlists_delete(self, kind: str or int, user_id: str = None,
                               timeout=None, *args, **kwargs):
        """Удаление плейлиста.

        Args:
            kind (:obj:`str` | :obj:`int`): Уникальный идентификатор плейлиста.
            user_id: (:obj:`int`, optional): Уникальный идентификатор пользователя владеющим плейлистом.
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`bool`: :obj:`True` при успешном выполнении запроса, иначе :obj:`False`.

        Raises:
            :class:`yandex_music.YandexMusicError`
        """

        if user_id is None:
            user_id = self.account.uid

        url = f'{self.base_url}/users/{user_id}/playlists/{kind}/delete'

        result = self._request.post(url, timeout=timeout, *args, **kwargs)

        return result == 'ok'

    def users_playlists_name(self, kind: str or int, name: str, user_id: str = None, timeout=None, *args, **kwargs):
        """Изменение названия плейлиста.

        Args:
            kind (:obj:`str` | :obj:`int`): Уникальный идентификатор плейлиста.
            name (:obj:`str`): Новое название.
            user_id: (:obj:`int`, optional): Уникальный идентификатор пользователя владеющим плейлистом.
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.Playlist`: Объекта класса :class:`yandex_music.Playlist`
            представляющий изменённый плейлист, иначе :obj:`None`.

        Raises:
            :class:`yandex_music.YandexMusicError`
        """

        if user_id is None:
            user_id = self.account.uid

        url = f'{self.base_url}/users/{user_id}/playlists/{kind}/name'

        result = self._request.post(url, {'value': name}, timeout=timeout, *args, **kwargs)

        return Playlist.de_json(result, self)

    def users_playlists_change(self, kind: str or int, diff: str, revision: int = 1, user_id: str = None,
                               timeout=None, *args, **kwargs):
        """Изменение плейлиста.

        Для получения отличий есть вспомогательный класс :class:`from yandex_music.utils.difference.Difference`.
        Так же существуют уже готовые методы-обёртки над операциями.

        Args:
            kind (:obj:`str` | :obj:`int`): Уникальный идентификатор плейлиста.
            revision (:obj:`int`): TODO.
            diff (:obj:`str`): JSON представления отличий старого и нового плейлиста.
            user_id: (:obj:`int`, optional): Уникальный идентификатор пользователя владеющим плейлистом.
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.Playlist`: Объекта класса :class:`yandex_music.Playlist`
            представляющий изменённый плейлист, иначе :obj:`None`.

        Raises:
            :class:`yandex_music.YandexMusicError`
        """

        if user_id is None:
            user_id = self.account.uid

        url = f'{self.base_url}/users/{user_id}/playlists/{kind}/change'

        data = {
            'kind': kind,
            'revision': revision,
            'diff': diff
        }

        result = self._request.post(url, data, timeout=timeout, *args, **kwargs)

        return Playlist.de_json(result, self)

    def users_playlists_insert_track(self, kind: str or int, track_id: str or int, album_id: str or int, at: int = 0,
                                     revision: int = 1, user_id: str = None, timeout=None, *args, **kwargs):
        """Добавление трека в плейлист.

        Трек можно вставить с любое место плейлиста задав индекс вставки (аргумент at).

        Args:
            kind (:obj:`str` | :obj:`int`): Уникальный идентификатор плейлиста.
            track_id (:obj:`str` | :obj:`int`): Уникальный идентификатор трека.
            album_id (:obj:`str` | :obj:`int`): Уникальный идентификатор альбома.
            at (:obj:`int`): Индекс для вставки.
            revision (:obj:`int`): TODO.
            user_id: (:obj:`int`, optional): Уникальный идентификатор пользователя владеющим плейлистом.
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.Playlist`: Объекта класса :class:`yandex_music.Playlist`
            представляющий изменённый плейлист, иначе :obj:`None`.

        Raises:
            :class:`yandex_music.YandexMusicError`
        """

        if user_id is None:
            user_id = self.account.uid

        diff = Difference().add_insert(at, {'id': track_id, 'album_id': album_id})

        return self.users_playlists_change(kind, diff.to_json(), revision, user_id, timeout, *args, **kwargs)

    def users_playlists_delete_track(self, kind: str or int, from_: int, to: int, revision: int = 1,
                                     user_id: str = None, timeout=None, *args, **kwargs):
        """Удаление треков из плейлиста.

        Для удаление необходимо указать границы с какого по какой элемент (трек) удалить.

        Args:
            kind (:obj:`str` | :obj:`int`): Уникальный идентификатор плейлиста.
            from_ (:obj:`int`): С какого индекса.
            to (:obj:`int`): По какой индекс.
            revision (:obj:`int`): TODO.
            user_id: (:obj:`int`, optional): Уникальный идентификатор пользователя владеющим плейлистом.
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.Playlist`: Объекта класса :class:`yandex_music.Playlist`
            представляющий изменённый плейлист, иначе :obj:`None`.

        Raises:
            :class:`yandex_music.YandexMusicError`
        """

        if user_id is None:
            user_id = self.account.uid

        diff = Difference().add_delete(from_, to)

        return self.users_playlists_change(kind, diff.to_json(), revision, user_id, timeout, *args, **kwargs)

    def rotor_account_status(self, timeout=None, *args, **kwargs):
        url = f'{self.base_url}/rotor/account/status'

        result = self._request.get(url, timeout=timeout, *args, **kwargs)

        return Status.de_json(result, self)

    def rotor_stations_dashboard(self, timeout=None, *args, **kwargs):
        url = f'{self.base_url}/rotor/stations/dashboard'

        result = self._request.get(url, timeout=timeout, *args, **kwargs)

        return Dashboard.de_json(result, self)

    def rotor_stations_list(self, language: str = 'en', timeout=None, *args, **kwargs):
        url = f'{self.base_url}/rotor/stations/list'

        result = self._request.get(url, {'language': language}, timeout=timeout, *args, **kwargs)

        return StationResult.de_list(result, self)

    def rotor_station_genre_feedback(self, genre: str, type_: str, timestamp=None, from_: str = None,
                                     batch_id: str or int = None, track_id: str = None, timeout=None, *args, **kwargs):
        if timestamp is None:
            timestamp = datetime.now().timestamp()

        url = f'{self.base_url}/rotor/station/genre:{genre}/feedback'

        params = {}
        data = {
            'type': type_,
            'timestamp': timestamp
        }

        if batch_id and track_id:
            data.update({'trackId': track_id})
            params = {'batch-id': batch_id}

        if from_:
            data.update({'from': from_})

        result = self._request.post(url, params=params, json=data, timeout=timeout, *args, **kwargs)

        return result == 'ok'

    def rotor_station_genre_feedback_radio_started(self, genre: str, from_: str, timestamp=None,
                                                   timeout=None, *args, **kwargs):
        return self.rotor_station_genre_feedback(genre, 'radioStarted', timestamp, from_, timeout, *args, **kwargs)

    def rotor_station_genre_feedback_track_started(self, genre: str, track_id: str, batch_id: str or int,
                                                   timestamp=None, timeout=None, *args, **kwargs):
        return self.rotor_station_genre_feedback(genre, 'trackStarted', timestamp, track_id=track_id, batch_id=batch_id,
                                                 timeout=timeout, *args, **kwargs)

    def rotor_station_genre_info(self, genre: str, timeout=None, *args, **kwargs):
        url = f'{self.base_url}/rotor/station/genre:{genre}/info'

        result = self._request.get(url, timeout=timeout, *args, **kwargs)

        return StationResult.de_list(result, self)

    def rotor_station_genre_tracks(self, genre: str, timeout=None, *args, **kwargs):
        url = f'{self.base_url}/rotor/station/genre:{genre}/tracks'

        result = self._request.get(url, timeout=timeout, *args, **kwargs)

        return StationTracksResult.de_json(result, self)

    def _like_action(self, object_type: str, ids: str or int or list, remove: bool = False, user_id: str or int = None,
                     timeout=None, *args, **kwargs):
        if user_id is None:
            user_id = self.account.uid

        action = 'remove' if remove else 'add-multiple'
        url = f'{self.base_url}/users/{user_id}/likes/{object_type}s/{action}'

        result = self._request.post(url, {f'{object_type}-ids': ids}, timeout=timeout, *args, **kwargs)

        if object_type == 'track':
            return 'revision' in result

        return result == 'ok'

    def users_likes_tracks_add(self, track_ids: str or list, user_id: str or int = None,
                               timeout=None, *args, **kwargs):
        return self._like_action('track', track_ids, user_id, timeout, *args, **kwargs)

    def users_likes_tracks_remove(self, track_ids: str or list, user_id: str or int = None,
                                  timeout=None, *args, **kwargs):
        return self._like_action('track', track_ids, True, user_id, timeout, *args, **kwargs)

    def users_likes_artists_add(self, artist_ids: str or int or list, user_id: str or int = None,
                                timeout=None, *args, **kwargs):
        return self._like_action('artist', artist_ids, user_id, timeout, *args, **kwargs)

    def users_likes_artists_remove(self, artist_ids: str or list, user_id: str or int = None,
                                   timeout=None, *args, **kwargs):
        return self._like_action('artist', artist_ids, True, user_id, timeout, *args, **kwargs)

    def users_likes_playlists_add(self, playlist_ids: str or list, user_id: str or int = None,
                                  timeout=None, *args, **kwargs):
        return self._like_action('playlist', playlist_ids, user_id, timeout, *args, **kwargs)

    def users_likes_playlists_remove(self, playlist_ids: str or list, user_id: str or int = None,
                                     timeout=None, *args, **kwargs):
        return self._like_action('playlist', playlist_ids, True, user_id, timeout, *args, **kwargs)

    def users_likes_albums_add(self, album_ids: str or list, user_id: str or int = None,
                               timeout=None, *args, **kwargs):
        return self._like_action('album', album_ids, user_id, timeout, *args, **kwargs)

    def users_likes_albums_remove(self, album_ids: str or list, user_id: str or int = None,
                                  timeout=None, *args, **kwargs):
        return self._like_action('album', album_ids, True, user_id, timeout, *args, **kwargs)

    def _get_list(self, object_type: str, ids: list or int or str, params=None, timeout=None, *args, **kwargs):
        if params is None:
            params = {}
        params.update({f'{object_type}-ids': ids})

        url = f'{self.base_url}/{object_type}s' + ('/list' if object_type == 'playlist' else '')

        result = self._request.post(url, params, timeout=timeout, *args, **kwargs)

        return de_list.get(object_type)(result, self)

    def artists(self, artist_ids: list or int or str, timeout=None, *args, **kwargs):
        return self._get_list('artist', artist_ids, timeout, *args, **kwargs)

    def albums(self, album_ids: list or int or str, timeout=None, *args, **kwargs):
        return self._get_list('album', album_ids, timeout, *args, **kwargs)

    def tracks(self, track_ids: int or str, with_positions=True, timeout=None, *args, **kwargs):
        return self._get_list('track', track_ids, {'with-positions': with_positions}, timeout, *args, **kwargs)

    def playlists_list(self, playlist_ids: list or int or str, timeout=None, *args, **kwargs):
        return self._get_list('playlist', playlist_ids, timeout, *args, **kwargs)

    def users_playlists_list(self, user_id: int or str = None, timeout=None, *args, **kwargs):
        if user_id is None:
            user_id = self.account.uid

        url = f'{self.base_url}/users/{user_id}/playlists/list'

        result = self._request.get(url, timeout=timeout, *args, **kwargs)

        return Playlist.de_list(result, self)

    def _get_likes(self, object_type, user_id: int or str = None, params=None, timeout=None, *args, **kwargs):
        if user_id is None:
            user_id = self.account.uid

        url = f'{self.base_url}/users/{user_id}/likes/{object_type}s'

        result = self._request.get(url, params, timeout=timeout, *args, **kwargs)

        if object_type == 'track':
            return TracksList.de_json(result.get('library'), self)

        return de_list_likes.get(object_type)(result, self)

    def users_likes_tracks(self, user_id: int or str = None, if_modified_since_revision=0, timeout=None,
                           *args, **kwargs):
        return self._get_likes('track', user_id, {'if-modified-since-revision': if_modified_since_revision}, timeout,
                               *args, **kwargs)

    def users_likes_albums(self, user_id: int or str = None, rich=True, timeout=None, *args, **kwargs):
        return self._get_likes('album', user_id, {'rich': rich}, timeout, *args, **kwargs)

    def users_likes_artists(self, user_id: int or str = None, with_timestamps=True, timeout=None, *args, **kwargs):
        return self._get_likes('artist', user_id, {'with-timestamps': with_timestamps}, timeout, *args, **kwargs)

    def users_likes_playlists(self, user_id: int or str = None, timeout=None, *args, **kwargs):
        return self._get_likes('playlist', user_id, timeout=timeout, *args, **kwargs)

    def users_dislikes_tracks(self, user_id: int or str = None, if_modified_since_revision=0,
                              timeout=None, *args, **kwargs):
        if user_id is None:
            user_id = self.account.uid

        url = f'{self.base_url}/users/{user_id}/dislikes/tracks'

        result = self._request.get(url, {'if_modified_since_revision': if_modified_since_revision},
                                   timeout=timeout, *args, **kwargs)

        return TracksList.de_json(result.get('library'), self)

    def _dislike_action(self, ids: str or int or list, remove: bool = False, user_id: str or int = None,
                        timeout=None, *args, **kwargs):
        if user_id is None:
            user_id = self.account.uid

        action = 'remove' if remove else 'add-multiple'
        url = f'{self.base_url}/users/{user_id}/dislikes/tracks/{action}'

        result = self._request.post(url, {f'track-ids': ids}, timeout=timeout, *args, **kwargs)

        return 'revision' in result

    def users_dislikes_tracks_add(self, track_ids: str or list, user_id: str or int = None,
                                  timeout=None, *args, **kwargs):
        return self._dislike_action(track_ids, user_id, timeout, *args, **kwargs)

    def users_dislikes_tracks_remove(self, track_ids: str or list, user_id: str or int = None,
                                     timeout=None, *args, **kwargs):
        return self._dislike_action(track_ids, True, user_id, timeout, *args, **kwargs)
