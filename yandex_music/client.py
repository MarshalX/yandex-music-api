import functools
import logging
from datetime import datetime
from typing import Callable, Dict, List, Optional, Union

from yandex_music import Album, Artist, ArtistAlbums, ArtistTracks, BriefInfo, Dashboard, DownloadInfo, Experiments, \
    Feed, Genre, Landing, Like, PermissionAlerts, Playlist, PromoCodeStatus, Search, Settings, ShotEvent, SimilarTracks, \
    StationResult, StationTracksResult, Status, Suggestions, Supplement, Track, TracksList, UserSettings, \
    YandexMusicObject
from yandex_music.exceptions import Captcha, InvalidToken
from yandex_music.utils.difference import Difference
from yandex_music.utils.request import Request

CLIENT_ID = '23cabbbdc6cd418abb4b39c32c41195d'
CLIENT_SECRET = '53bc75238f0c4d08a118e51fe9203300'

de_list = {
    'artist': Artist.de_list,
    'album': Album.de_list,
    'track': Track.de_list,
    'playlist': Playlist.de_list,
}

logging.getLogger(__name__).addHandler(logging.NullHandler())


def log(method):
    logger = logging.getLogger(method.__module__)

    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        logger.debug(f'Entering: {method.__name__}')

        result = method(*args, **kwargs)
        logger.debug(result)

        logger.debug(f'Exiting: {method.__name__}')

        return result

    return wrapper


class Client(YandexMusicObject):
    """Класс, представляющий клиент Yandex Music.

    Note:
        При `fetch_account_status = False` многие сокращения перестанут работать в связи с тем, что неоткуда будет взять
        uid аккаунта для отправки запроса. Так же в большинстве методов придётся передавать `uid` явно.

    Attributes:
        logger (:obj:`logging.Logger`): Объект логера.
        token (:obj:`str`): Уникальный ключ для аутентификации.
        base_url (:obj:`str`): Ссылка на API Yandex Music.
        oauth_url (:obj:`str`): Ссылка на OAuth Yandex Music.
        me (:obj:`yandex_music.Status`): Информация об аккаунте.

    Args:
        token (:obj:`str`, optional): Уникальный ключ для аутентификации.
        fetch_account_status (:obj:`bool`, optional): Получить ли информацию об аккаунте при инициализации объекта.
        base_url (:obj:`str`, optional): Ссылка на API Yandex Music.
        oauth_url (:obj:`str`, optional): Ссылка на OAuth Yandex Music.
        request (:obj:`yandex_music.utils.request.Request`, optional): Пре-инициализация
            :class:`yandex_music.utils.request.Request`.
    """

    def __init__(self, token: str = None, fetch_account_status: bool = True, base_url: str = None,
                 oauth_url: str = None, request: Request = None) -> None:
        self.logger = logging.getLogger(__name__)
        self.token = token

        if base_url is None:
            base_url = 'https://api.music.yandex.net'
        if oauth_url is None:
            oauth_url = 'https://oauth.yandex.ru'

        self.base_url = base_url
        self.oauth_url = oauth_url

        if request:
            self._request = request
            self._request.set_and_return_client(self)
        else:
            self._request = Request(self)

        self.me = None
        if fetch_account_status:
            self.me = self.account_status()

    @classmethod
    def from_credentials(cls, username: str, password: str, x_captcha_answer: str = None, x_captcha_key: str = None,
                         captcha_callback: Callable[[Captcha], str] = None, *args, **kwargs) -> 'Client':
        """Инициализция клиента по логину и паролю.

        Note:
            Данный метод получает токен каждый раз при вызове. Рекомендуется сгенерировать его самостоятельно, сохранить
            и использовать при следующих инициализациях клиента. Не храните логины и пароли!

        Args:
            username (:obj:`str`): Логин клиента (идентификатор).
            password (:obj:`str`): Пароль клиента (аутентификатор).
            x_captcha_answer (:obj:`str`, optional): Ответ на капчу (цифры с картинки).
            x_captcha_key (:obj:`str`, optional): Уникальный ключ капчи.
            captcha_callback (:obj:`function`, optional): Функция обратного вызова для обработки капчи, должна
                принимать объект класса :class:`yandex_music.exceptions.Captcha` и возвращать проверочный код.
            **kwargs (:obj:`dict`, optional): Аргументы для конструктора клиента.

        Returns:
            :obj:`yandex_music.Client`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """

        token = None
        while not token:
            try:
                token = cls(*args, **kwargs).generate_token_by_username_and_password(username, password,
                                                                                     x_captcha_answer=x_captcha_answer,
                                                                                     x_captcha_key=x_captcha_key)
            except Captcha as e:
                if not captcha_callback:
                    raise e

                x_captcha_answer = captcha_callback(e.captcha)
                x_captcha_key = e.captcha.x_captcha_key

        return cls(token, *args, **kwargs)

    @classmethod
    def from_token(cls, token: str, *args, **kwargs) -> 'Client':
        """Инициализция клиента по токену.

        Note:
            Ничем не отличается от `Client(token)`. Так исторически сложилось.

        Args:
            token (:obj:`str`, optional): Уникальный ключ для аутентификации.
            **kwargs (:obj:`dict`, optional): Аргументы для конструктора клиента.

        Returns:
            :obj:`yandex_music.Client`.
        """

        return cls(token, *args, **kwargs)

    @log
    def generate_token_by_username_and_password(self, username: str, password: str, grant_type: str = 'password',
                                                x_captcha_answer: str = None, x_captcha_key: str = None,
                                                timeout: Union[int, float] = None, *args, **kwargs) -> str:
        """Метод получения OAuth токена по логину и паролю.

        Args:
            username (:obj:`str`): Логин клиента (идентификатор).
            password (:obj:`str`): Пароль клиента (аутентификатор).
            grant_type (:obj:`str`, optional): Тип разрешения OAuth.
            x_captcha_answer (:obj:`str`, optional): Ответ на капчу (цифры с картинки).
            x_captcha_key (:obj:`str`, optional): Уникальный ключ капчи.
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`str`: OAuth токен.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """

        url = f'{self.oauth_url}/token'

        data = {
            'grant_type': grant_type,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'username': username,
            'password': password
        }

        if x_captcha_answer and x_captcha_key:
            data.update({'x_captcha_answer': x_captcha_answer, 'x_captcha_key': x_captcha_key})

        result = self._request.post(url, data, timeout=timeout, *args, **kwargs)

        return result.get('access_token')

    @staticmethod
    def _validate_token(token: str) -> str:
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
    def request(self) -> Request:
        """:obj:`yandex_music.utils.request.Request`: Объект вспомогательного класса для отправки запросов."""
        return self._request

    @log
    def account_status(self, timeout: Union[int, float] = None, *args, **kwargs) -> Optional[Status]:
        """Получение статуса аккаунта. Нет обязательных параметров.

        Args:
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.Status` | :obj:`None`: Информация об аккаунте если он валиден, иначе :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """

        url = f'{self.base_url}/account/status'

        result = self._request.get(url, timeout=timeout, *args, **kwargs)

        return Status.de_json(result, self)

    @log
    def account_settings(self, timeout: Union[int, float] = None, *args, **kwargs) -> Optional[UserSettings]:
        """Получение настроек текущего пользователя.

        Args:
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.UserSettings` | :obj:`None`: Настройки пользователя если аккаунт валиден,
                иначе :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """

        url = f'{self.base_url}/account/settings'

        result = self._request.get(url, timeout=timeout, *args, **kwargs)

        return UserSettings.de_json(result, self)

    @log
    def account_settings_set(self, param: str = None, value: Union[str, int, bool] = None,
                             data: Dict[str, Union[str, int, bool]] = None, timeout: Union[int, float] = None,
                             *args, **kwargs) -> Optional[UserSettings]:
        """Изменение настроек текущего пользователя.

        Note:
            Доступные названия параметров есть поля в классе :class:`yandex_music.UserSettings`, только в CamelCase.

        Args:
            param (:obj:`str`): Название параметра для изменения.
            value (:obj:`str` | :obj:`int` | :obj:`bool`): Значение параметра.
            data (:obj:`dict`): Словарь параметров и значений для множественного изменения.
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.UserSettings` | :obj:`None`: Настройки пользователя или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """

        url = f'{self.base_url}/account/settings'

        if not data:
            data = {param: value}

        result = self._request.post(url, data=data, timeout=timeout, *args, **kwargs)

        return UserSettings.de_json(result, self)

    @log
    def settings(self, timeout: Union[int, float] = None, *args, **kwargs) -> Optional[Settings]:
        """Получение предложений по покупке. Нет обязательных параметров.

        Args:
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.Settings` | :obj:`None`: Информацию о предлагаемых продуктах если аккаунт валиден
                или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """

        url = f'{self.base_url}/settings'

        result = self._request.get(url, timeout=timeout, *args, **kwargs)

        return Settings.de_json(result, self)

    @log
    def permission_alerts(self, timeout: Union[int, float] = None, *args, **kwargs) -> Optional[PermissionAlerts]:
        """Получение оповещений. Нет обязательных параметров.

        Args:
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.PermissionAlerts` | :obj:`None`: Оповещения если аккаунт валиден или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """

        url = f'{self.base_url}/permission-alerts'

        result = self._request.get(url, timeout=timeout, *args, **kwargs)

        return PermissionAlerts.de_json(result, self)

    @log
    def account_experiments(self, timeout: Union[int, float] = None, *args, **kwargs) -> Optional[Experiments]:
        """Получение значений экспериментальных функций аккаунта.

        Args:
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.Experiments` | :obj:`None`: Состояние экспериментальных функций или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """

        url = f'{self.base_url}/account/experiments'

        result = self._request.get(url, timeout=timeout, *args, **kwargs)

        return Experiments.de_json(result, self)

    @log
    def consume_promo_code(self, code: str, language: str = 'en', timeout: Union[int, float] = None,
                           *args, **kwargs) -> Optional[PromoCodeStatus]:
        """Активация промо-кода.

        Args:
            code (:obj:`str`): Промо-код.
            language (:obj:`str`, optional): Язык ответа API в ISO 639-1.
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.PromoCodeStatus` | :obj:`None`: Информация об активации промо-кода или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """

        url = f'{self.base_url}/account/consume-promo-code'

        result = self._request.post(url, {'code': code, 'language': language}, timeout=timeout, *args, **kwargs)

        return PromoCodeStatus.de_json(result, self)

    @log
    def feed(self, timeout: Union[int, float] = None, *args, **kwargs) -> Optional[Feed]:
        """Получение потока информации (фида) подобранного под пользователя. Содержит умные плейлисты.

        Args:
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.Feed` | :obj:`None`: Умные плейлисты пользователя или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """

        url = f'{self.base_url}/feed'

        result = self._request.get(url, timeout=timeout, *args, **kwargs)

        return Feed.de_json(result, self)

    @log
    def feed_wizard_is_passed(self, timeout: Union[int, float] = None, *args, **kwargs) -> bool:
        url = f'{self.base_url}/feed/wizard/is-passed'

        result = self._request.get(url, timeout=timeout, *args, **kwargs)

        return result.get('is_wizard_passed') or False

    @log
    def landing(self, blocks: Union[str, List[str]], timeout: Union[int, float] = None,
                *args, **kwargs) -> Optional[Landing]:
        """Получение лендинг-страницы содержащий блоки с новыми релизами, чартами, плейлистами с новинками и т.д.

        Note:
            Поддерживаемые типы блоков: `personalplaylists`, `promotions`, `new-releases`, `new-playlists`, `mixes`,
            `chart`, `artists`, `albums`, `playlists`, `play_contexts`.

        Args:
            blocks (:obj:`str` | :obj:`list` из :obj:`str`): Блок или список блоков необходимых для выдачи.
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.Landing` | :obj:`None`: Лендинг-страница или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """

        url = f'{self.base_url}/landing3'

        result = self._request.get(url, {'blocks': blocks}, timeout=timeout, *args, **kwargs)

        return Landing.de_json(result, self)

    @log
    def genres(self, timeout: Union[int, float] = None, *args, **kwargs) -> List[Genre]:
        """Получение жанров музыки.

        Args:
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`list` из :obj:`yandex_music.Genre` | :obj:`None`: Жанры музыки или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """

        url = f'{self.base_url}/genres'

        result = self._request.get(url, timeout=timeout, *args, **kwargs)

        return Genre.de_list(result, self)

    @log
    def tracks_download_info(self, track_id: Union[str, int], get_direct_links: bool = False,
                             timeout: Union[int, float] = None, *args, **kwargs) -> List[DownloadInfo]:
        """Получение информации о доступных вариантах загрузки трека.

        Args:
            track_id (:obj:`str` | :obj:`list` из :obj:`str`): Уникальный идентификатор трека или треков.
            get_direct_links (:obj:`bool`, optional): Получить ли при вызове метода прямую ссылку на загрузку.
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`list` из :obj:`yandex_music.DownloadInfo` | :obj:`None`: Варианты загрузки трека или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """

        url = f'{self.base_url}/tracks/{track_id}/download-info'

        result = self._request.get(url, timeout=timeout, *args, **kwargs)

        return DownloadInfo.de_list(result, self, get_direct_links)

    @log
    def track_supplement(self, track_id: Union[str, int], timeout: Union[int, float] = None,
                         *args, **kwargs) -> Optional[Supplement]:
        """Получение дополнительной информации о треке.

        Args:
            track_id (:obj:`str`): Уникальный идентификатор трека.
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.Supplement`: Дополнительная информация о треке.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """

        url = f'{self.base_url}/tracks/{track_id}/supplement'

        result = self._request.get(url, timeout=timeout, *args, **kwargs)

        return Supplement.de_json(result, self)

    @log
    def tracks_similar(self, track_id: Union[str, int], timeout: Union[int, float] = None,
                       *args, **kwargs) -> Optional[SimilarTracks]:
        """Получение похожих треков.

        Args:
            track_id (:obj:`str`): Уникальный идентификатор трека.
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.SimilarTracks`: Похожие треки на другой трек.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """

        url = f'{self.base_url}/tracks/{track_id}/similar'

        result = self._request.get(url, timeout=timeout, *args, **kwargs)

        return SimilarTracks.de_json(result, self)

    @log
    def play_audio(self,
                   track_id: Union[str, int],
                   from_: str,
                   album_id: Union[str, int],
                   playlist_id: str = None,
                   from_cache: bool = False,
                   play_id: str = None,
                   uid: int = None,
                   timestamp: str = None,
                   track_length_seconds: int = 0,
                   total_played_seconds: int = 0,
                   end_position_seconds: int = 0,
                   client_now: str = None,
                   timeout: Union[int, float] = None,
                   *args, **kwargs) -> bool:
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
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """

        if uid is None and self.me is not None:
            uid = self.me.account.uid

        url = f'{self.base_url}/play-audio'

        data = {
            'track-id': track_id,
            'from-cache': from_cache,
            'from': from_,
            'play-id': play_id or '',
            'uid': uid,
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

    def albums_with_tracks(self, album_id: Union[str, int], timeout: Union[int, float] = None,
                           *args, **kwargs) -> Optional[Album]:
        """Получение альбома по его уникальному идентификатору вместе с треками.

        Args:
            album_id (:obj:`str` | :obj:`int`): Уникальный идентификатор альбома.
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`list` из :obj:`yandex_music.Album` | :obj:`None`: Альбом или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """

        url = f'{self.base_url}/albums/{album_id}/with-tracks'

        result = self._request.get(url, timeout=timeout, *args, **kwargs)

        return Album.de_json(result, self)

    @log
    def search(self,
               text: str,
               nocorrect: bool = False,
               type_: str = 'all',
               page: int = 0,
               playlist_in_best: bool = True,
               timeout: Union[int, float] = None,
               *args, **kwargs) -> Optional[Search]:
        """Осуществление поиска по запросу и типу, получение результатов.

        Args:
            text (:obj:`str`): Текст запроса.
            nocorrect (:obj:`bool`): Если :obj:`False`, то ошибочный запрос будет исправлен. Например, запрос
                "Гражданская абарона" будет исправлен на "Гражданская оборона".
            type_ (:obj:`str`): Среди какого типа искать (трек, плейлист, альбом, исполнитель).
            page (:obj:`int`): Номер страницы.
            playlist_in_best (:obj:`bool`): Выдавать ли плейлисты лучшим вариантом поиска.
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.Search` | :obj:`None`: Результаты поиска или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
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

    @log
    def search_suggest(self, part: str, timeout: Union[int, float] = None,
                       *args, **kwargs) -> Optional[Suggestions]:
        """Получение подсказок по введенной части поискового запроса.

        Args:
            part (:obj:`str`): Часть поискового запроса.
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.Suggestions` | :obj:`None`: Подсказки для запроса или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """

        url = f'{self.base_url}/search/suggest'

        result = self._request.get(url, {'part': part}, timeout=timeout, *args, **kwargs)

        return Suggestions.de_json(result, self)

    @log
    def users_settings(self, user_id: Union[str, int] = None, timeout: Union[int, float] = None,
                       *args, **kwargs) -> Optional[UserSettings]:
        """Получение настроек пользователя.

        Note:
            Для получения настроек пользователя нужно быть авторизованным или владеть `user_id`.

        Args:
            user_id (:obj:`str` | :obj:`int`, optional): Уникальный идентификатор пользователя чьи настройки хотим
                получить.
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.UserSettings` | :obj:`None`: Настройки пользователя или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """

        if user_id is None and self.me is not None:
            user_id = self.me.account.uid

        url = f'{self.base_url}/users/{user_id}/settings'

        result = self._request.get(url, timeout=timeout, *args, **kwargs)

        return UserSettings.de_json(result.get('user_settings'), self)

    @log
    def users_playlists(self, kind: Union[List[Union[str, int]], str, int], user_id: Union[str, int] = None,
                        timeout: Union[int, float] = None, *args, **kwargs) -> List[Playlist]:
        """Получение плейлиста или списка плейлистов по уникальным идентификаторам.

        Args:
            kind (:obj:`str` | :obj:`int` | :obj:`list` из :obj:`str` | :obj:`int`): Уникальный идентификатор плейлиста
                или их список.
            user_id (:obj:`str` | :obj:`int`, optional): Уникальный идентификатор пользователя владеющим плейлистом.
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`list` из :obj:`yandex_music.Playlist` | :obj:`None`: Плейлист или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """

        if user_id is None and self.me is not None:
            user_id = self.me.account.uid

        url = f'{self.base_url}/users/{user_id}/playlists'

        data = {
            'kinds': kind
        }

        result = self._request.post(url, data, timeout=timeout, *args, **kwargs)

        return Playlist.de_list(result, self)

    @log
    def users_playlists_create(self, title: str, visibility: str = 'public', user_id: Union[str, int] = None,
                               timeout: Union[int, float] = None, *args, **kwargs) -> Optional[Playlist]:
        """Создание плейлиста.

        Args:
            title (:obj:`str`): Название.
            visibility (:obj:`str`, optional): Модификатор доступа.
            user_id (:obj:`str` | :obj:`int`, optional): Уникальный идентификатор пользователя владеющим плейлистом.
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.Playlist` | :obj:`None`: Созданный плейлист или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """

        if user_id is None and self.me is not None:
            user_id = self.me.account.uid

        url = f'{self.base_url}/users/{user_id}/playlists/create'

        data = {
            'title': title,
            'visibility': visibility
        }

        result = self._request.post(url, data, timeout=timeout, *args, **kwargs)

        return Playlist.de_json(result, self)

    @log
    def users_playlists_delete(self, kind: Union[str, int], user_id: Union[str, int] = None,
                               timeout: Union[int, float] = None, *args, **kwargs) -> bool:
        """Удаление плейлиста.

        Args:
            kind (:obj:`str` | :obj:`int`): Уникальный идентификатор плейлиста.
            user_id (:obj:`str` | :obj:`int`, optional): Уникальный идентификатор пользователя владеющим плейлистом.
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`bool`: :obj:`True` при успешном выполнении запроса, иначе :obj:`False`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """

        if user_id is None and self.me is not None:
            user_id = self.me.account.uid

        url = f'{self.base_url}/users/{user_id}/playlists/{kind}/delete'

        result = self._request.post(url, timeout=timeout, *args, **kwargs)

        return result == 'ok'

    @log
    def users_playlists_name(self, kind: Union[str, int], name: str, user_id: Union[str, int] = None,
                             timeout: Union[int, float] = None, *args, **kwargs) -> Optional[Playlist]:
        """Изменение названия плейлиста.

        Args:
            kind (:obj:`str` | :obj:`int`): Уникальный идентификатор плейлиста.
            name (:obj:`str`): Новое название.
            user_id (:obj:`str` | :obj:`int`, optional): Уникальный идентификатор пользователя владеющим плейлистом.
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.Playlist` | :obj:`None`: Изменённый плейлист или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """

        if user_id is None and self.me is not None:
            user_id = self.me.account.uid

        url = f'{self.base_url}/users/{user_id}/playlists/{kind}/name'

        result = self._request.post(url, {'value': name}, timeout=timeout, *args, **kwargs)

        return Playlist.de_json(result, self)

    @log
    def users_playlists_visibility(self, kind: Union[str, int], visibility: str, user_id: Union[str, int] = None,
                                   timeout: Union[int, float] = None, *args, **kwargs) -> Optional[Playlist]:
        """Изменение видимости плейлиста.

        Note:
            Видимость (`visibility`) может быть задана только одним из двух значений: `private`, `public`.

        Args:
            kind (:obj:`str` | :obj:`int`): Уникальный идентификатор плейлиста.
            visibility (:obj:`str`): Новое название.
            user_id (:obj:`str` | :obj:`int`, optional): Уникальный идентификатор пользователя владеющим плейлистом.
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.Playlist` | :obj:`None`: Изменённый плейлист или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """

        if user_id is None and self.me is not None:
            user_id = self.me.account.uid

        url = f'{self.base_url}/users/{user_id}/playlists/{kind}/visibility'

        result = self._request.post(url, {'value': visibility}, timeout=timeout, *args, **kwargs)

        return Playlist.de_json(result, self)

    @log
    def users_playlists_change(self, kind: Union[str, int], diff: str, revision: int = 1,
                               user_id: Union[str, int] = None, timeout: Union[int, float] = None,
                               *args, **kwargs) -> Optional[Playlist]:
        """Изменение плейлиста.

        Note:
            Для получения отличий есть вспомогательный класс :class:`yandex_music.utils.difference.Difference`.

            Так же существуют уже готовые методы-обёртки над операциями.

        Args:
            kind (:obj:`str` | :obj:`int`): Уникальный идентификатор плейлиста.
            revision (:obj:`int`): TODO.
            diff (:obj:`str`): JSON представления отличий старого и нового плейлиста.
            user_id (:obj:`str` | :obj:`int`, optional): Уникальный идентификатор пользователя владеющим плейлистом.
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.Playlist`: Изменённый плейлист или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """

        if user_id is None and self.me is not None:
            user_id = self.me.account.uid

        url = f'{self.base_url}/users/{user_id}/playlists/{kind}/change'

        data = {
            'kind': kind,
            'revision': revision,
            'diff': diff
        }

        result = self._request.post(url, data, timeout=timeout, *args, **kwargs)

        return Playlist.de_json(result, self)

    @log
    def users_playlists_insert_track(self, kind: Union[str, int], track_id: Union[str, int], album_id: Union[str, int],
                                     at: int = 0, revision: int = 1, user_id: Union[str, int] = None,
                                     timeout: Union[int, float] = None, *args, **kwargs) -> Optional[Playlist]:
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
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.Playlist`: Изменённый плейлист или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """

        if user_id is None and self.me is not None:
            user_id = self.me.account.uid

        diff = Difference().add_insert(at, {'id': track_id, 'album_id': album_id})

        return self.users_playlists_change(kind, diff.to_json(), revision, user_id, timeout, *args, **kwargs)

    @log
    def users_playlists_delete_track(self, kind: Union[str, int], from_: int, to: int, revision: int = 1,
                                     user_id: Union[str, int] = None, timeout: Union[int, float] = None,
                                     *args, **kwargs) -> Optional[Playlist]:
        """Удаление треков из плейлиста.

        Note:
            Для удаление необходимо указать границы с какого по какой элемент (трек) удалить.

        Args:
            kind (:obj:`str` | :obj:`int`): Уникальный идентификатор плейлиста.
            from_ (:obj:`int`): С какого индекса.
            to (:obj:`int`): По какой индекс.
            revision (:obj:`int`): TODO.
            user_id (:obj:`str` | :obj:`int`, optional): Уникальный идентификатор пользователя владеющим плейлистом.
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.Playlist` | :obj:`None`: Изменённый плейлист или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """

        if user_id is None and self.me is not None:
            user_id = self.me.account.uid

        diff = Difference().add_delete(from_, to)

        return self.users_playlists_change(kind, diff.to_json(), revision, user_id, timeout, *args, **kwargs)

    @log
    def rotor_account_status(self, timeout: Union[int, float] = None, *args, **kwargs) -> Optional[Status]:
        """Получение статуса пользователя с дополнителньыми полями.

        Note:
            Данный статус отличается от обычного наличием дополнительных полей, например, `skips_per_hour`.

        Args:
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.Status` | :obj:`None`: Статус пользователя с дополнительными полями от радио или
                :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """

        url = f'{self.base_url}/rotor/account/status'

        result = self._request.get(url, timeout=timeout, *args, **kwargs)

        return Status.de_json(result, self)

    @log
    def rotor_stations_dashboard(self, timeout: Union[int, float] = None,
                                 *args, **kwargs) -> Optional[Dashboard]:
        """Получение рекомендованных станций текущего пользователя.

        Args:
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.Dashboard` | :obj:`None`: Рекомендованные станции или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """

        url = f'{self.base_url}/rotor/stations/dashboard'

        result = self._request.get(url, timeout=timeout, *args, **kwargs)

        return Dashboard.de_json(result, self)

    @log
    def rotor_stations_list(self, language: str = 'ru', timeout: Union[int, float] = None,
                            *args, **kwargs) -> List[StationResult]:
        """Получение всех радиостанций с настройками пользователя.

        Note:
            Чтобы определить что за тип станции (жанры, настроения, занятие и т.д.) необходимо смотреть в поле
            `id_for_from`.

        Args:
            language (:obj:`str`): Язык, на котором будет информация о станциях.
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`list` из :obj:`yandex_music.StationResult` | :obj:`None`: Станции или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """

        url = f'{self.base_url}/rotor/stations/list'

        result = self._request.get(url, {'language': language}, timeout=timeout, *args, **kwargs)

        return StationResult.de_list(result, self)

    @log
    def rotor_station_feedback(self, station: str, type_: str, timestamp: Union[str, float, int] = None,
                               from_: str = None, batch_id: str = None, total_played_seconds: Union[int, float] = None,
                               track_id: Union[str, int] = None, timeout: Union[int, float] = None,
                               *args, **kwargs) -> bool:
        """Отправка ответной реакции на происходящее при прослушивании радио.

        Note:
            Сообщения о начале прослушивания радио, начале и конце трека, его пропуска.

            Известные типы фидбека: `radioStarted`, `trackStarted`, `trackFinished`, `skip`.

            Пример `station`: `user:onyourwave`, `genre:allrock`.

            Пример `from_`: `mobile-radio-user-123456789`.

        Args:
            station (:obj:`str`): Станция.
            type_ (:obj:`str`): Тип отправляемого фидбека.
            timestamp (:obj:`str` | :obj:`float` | :obj:`int`, optional): Текущее время и дата.
            from_ (:obj:`str`, optional): Откуда начато воспроизведение радио.
            batch_id (:obj:`str`, optional): Уникальный идентификатор партии треков. Возвращается при получении треков.
            total_played_seconds (:obj:`int` |:obj:`float`, optional): Сколько было проиграно секунд трека
                перед действием.
            track_id (:obj:`int` | :obj:`str`, optional): Уникальной идентификатор трека.
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`bool`: :obj:`True` при успешном выполнении запроса, иначе :obj:`False`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """

        if timestamp is None:
            timestamp = datetime.now().timestamp()

        url = f'{self.base_url}/rotor/station/{station}/feedback'

        params = {}
        data = {
            'type': type_,
            'timestamp': timestamp
        }

        if batch_id:
            params = {'batch-id': batch_id}

        if track_id:
            data.update({'trackId': track_id})

        if from_:
            data.update({'from': from_})

        if total_played_seconds:
            data.update({'totalPlayedSeconds': total_played_seconds})

        result = self._request.post(url, params=params, json=data, timeout=timeout, *args, **kwargs)

        return result == 'ok'

    @log
    def rotor_station_feedback_radio_started(self, station: str, from_: str, batch_id: str = None,
                                             timestamp: Union[str, float, int] = None,
                                             timeout: Union[int, float] = None, *args, **kwargs) -> bool:
        """Сокращение для::

            client.rotor_station_feedback(station, 'radioStarted', timestamp, from, *args, **kwargs)

        Returns:
            :obj:`bool`: :obj:`True` при успешном выполнении запроса, иначе :obj:`False`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        return self.rotor_station_feedback(station, 'radioStarted', timestamp, from_=from_, batch_id=batch_id,
                                           timeout=timeout, *args, **kwargs)

    @log
    def rotor_station_feedback_track_started(self, station: str, track_id: Union[str, int], batch_id: str = None,
                                             timestamp: Union[str, float, int] = None,
                                             timeout: Union[int, float] = None, *args, **kwargs) -> bool:
        """Сокращение для::

            client.rotor_station_feedback(station, 'trackStarted', timestamp, track_id, *args, **kwargs)

        Returns:
            :obj:`bool`: :obj:`True` при успешном выполнении запроса, иначе :obj:`False`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        return self.rotor_station_feedback(station, 'trackStarted', timestamp, track_id=track_id, batch_id=batch_id,
                                           timeout=timeout, *args, **kwargs)

    @log
    def rotor_station_feedback_track_finished(self, station: str, track_id: Union[str, int],
                                              total_played_seconds: float, batch_id: str = None,
                                              timestamp: Union[str, float, int] = None,
                                              timeout: Union[int, float] = None, *args, **kwargs) -> bool:
        """Сокращение для::

            client.rotor_station_feedback(station, 'trackFinished', timestamp, track_id, total_played_seconds,
            *args, **kwargs)

        Returns:
            :obj:`bool`: :obj:`True` при успешном выполнении запроса, иначе :obj:`False`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        return self.rotor_station_feedback(station, 'trackFinished', timestamp, track_id=track_id,
                                           total_played_seconds=total_played_seconds, batch_id=batch_id,
                                           timeout=timeout, *args, **kwargs)

    @log
    def rotor_station_feedback_skip(self, station: str, track_id: Union[str, int],
                                    total_played_seconds: float, batch_id: str = None,
                                    timestamp: Union[str, float, int] = None,
                                    timeout: Union[int, float] = None, *args, **kwargs) -> bool:
        """Сокращение для::

            client.rotor_station_feedback(station, 'skip', timestamp, track_id, total_played_seconds,
            *args, **kwargs)

        Returns:
            :obj:`bool`: :obj:`True` при успешном выполнении запроса, иначе :obj:`False`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        return self.rotor_station_feedback(station, 'skip', timestamp, track_id=track_id,
                                           total_played_seconds=total_played_seconds, batch_id=batch_id,
                                           timeout=timeout, *args, **kwargs)

    @log
    def rotor_station_info(self, station: str, timeout: Union[int, float] = None,
                           *args, **kwargs) -> List[StationResult]:
        """Получение информации о станции и пользовательских настроек на неё.

        Args:
            station (:obj:`str`): Станция.
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`list` из :obj:`yandex_music.StationResult` | :obj:`None`: Информация о станции или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """

        url = f'{self.base_url}/rotor/station/{station}/info'

        result = self._request.get(url, timeout=timeout, *args, **kwargs)

        return StationResult.de_list(result, self)

    @log
    def rotor_station_settings2(self, station: str, mood_energy: str, diversity: str, language: str = 'not-russian',
                                timeout: Union[int, float] = None, *args, **kwargs) -> bool:
        """Изменение настроек определённой станции.

        Note:
            Доступные значения для `mood_energy`: `fun`, `active`, `calm`, `sad`, `all`.

            Доступные значения для `diversity`: `favorite`, `popular`, `discover`, `default`.

            Доступные значения для `language`: `not-russian`, `russian`, `any`.

            У станций в `restrictions` есть Enum'ы, а в них `possible_values` - доступные значения для поля.

        Args:
            station (:obj:`str`): Станция.
            mood_energy (:obj:`str`): Настроение.
            diversity (:obj:`str`): Треки.
            language (:obj:`str`): Язык.
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`bool`: :obj:`True` при успешном выполнении запроса, иначе :obj:`False`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """

        url = f'{self.base_url}/rotor/station/{station}/settings2'

        data = {
            'moodEnergy': mood_energy,
            'diversity': diversity
        }

        if language:
            data.update({'language': language})

        result = self._request.post(url, json=data, timeout=timeout, *args, **kwargs)

        return result == 'ok'

    @log
    def rotor_station_tracks(self, station: str, settings2: bool = True, queue: Union[str, int] = None,
                             timeout: Union[int, float] = None, *args, **kwargs) -> Optional[StationTracksResult]:
        """Получение цепочки треков определённой станции.

        Note:
            Для продолжения цепочки треков необходимо:

            1. Передавать `ID` трека, что был до этого (первый в цепочки).
            2. Отправить фидбек о конче или скипе трека, что был передан в `queue`.
            3. Отправить фидбек о начале следующего трека (второй в цепочки).
            4. Выполнить запрос получения треков. В ответе придёт новые треки или произойдёт сдвиг цепочки на 1 элемент.

            Проход по цепочке до коцна не изучен. Часто встречаются дубликаты.

            Все официальные клиенты выполняют запросы с `settings2 = True`.

        Args:
            station (:obj:`str`): Станция.
            settings2 (:obj:`bool`, optional): Использовать ли второй набор настроек.
            queue (:obj:`str` | :obj:`int` , optional): Уникальной идентификатор трека, который только что был.
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.StationTracksResult` | :obj:`None`: Последовательность треков станции или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """

        url = f'{self.base_url}/rotor/station/{station}/tracks'

        params = {}
        if settings2:
            params = {'settings2': True}

        if queue:
            params = {'queue': queue}

        result = self._request.get(url, params=params, timeout=timeout, *args, **kwargs)

        return StationTracksResult.de_json(result, self)

    @log
    def artists_brief_info(self, artist_id: Union[str, int], timeout: Union[int, float] = None,
                           *args, **kwargs) -> Optional[BriefInfo]:
        """Получение информации об артисте.

        Args:
            artist_id (:obj:`str` | :obj:`int`): Уникальный идентификатор исполнителя.
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.BriefInfo` | :obj:`None`: Информация об артисте или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/artists/{artist_id}/brief-info'

        result = self._request.get(url, timeout=timeout, *args, **kwargs)

        return BriefInfo.de_json(result, self)

    @log
    def artists_tracks(self, artist_id: Union[str, int], page: int = 0, page_size: int = 20,
                       timeout: Union[int, float] = None, *args, **kwargs) -> Optional[ArtistTracks]:
        """Получение треков артиста.

        Args:
            artist_id (:obj:`str` | :obj:`int`): Уникальный идентификатор артиста.
            page (:obj:`int`, optional): Номер страницы.
            page_size (:obj:`int`, optional): Количество треков на странице.
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.ArtistsTracks` | :obj:`None`: Страница списка треков артиста или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """

        url = f'{self.base_url}/artists/{artist_id}/tracks'

        params = {
            'page': page,
            'page-size': page_size
        }

        result = self._request.get(url, params, timeout=timeout, *args, **kwargs)

        return ArtistTracks.de_json(result, self)

    @log
    def artists_direct_albums(self, artist_id: Union[str, int], page: int = 0, page_size: int = 20,
                              sort_by: str = 'year', timeout: Union[int, float] = None,
                              *args, **kwargs) -> Optional[ArtistAlbums]:
        """Получение альбомов артиста.

        Note:
            Известные значения для `sort_by`: `year`, `rating`.

        Args:
            artist_id (:obj:`str` | :obj:`int`): Уникальный идентификатор артиста.
            page (:obj:`int`, optional): Номер страницы.
            page_size (:obj:`int`, optional): Количество альбомов на странице.
            sort_by (:obj:`str`, optional): Параметр для сортировки.
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.ArtistAlbums` | :obj:`None`: Страница списка альбомов артиста или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """

        url = f'{self.base_url}/artists/{artist_id}/direct-albums'

        params = {
            'sort-by': sort_by,
            'page': page,
            'page-size': page_size
        }

        result = self._request.get(url, params, timeout=timeout, *args, **kwargs)

        return ArtistAlbums.de_json(result, self)

    def _like_action(self, object_type: str, ids: Union[List[Union[str, int]], str, int], remove: bool = False,
                     user_id: Union[str, int] = None, timeout: Union[int, float] = None, *args, **kwargs) -> bool:
        """Действия с отметкой "Мне нравится".

        Note:
            Типы объектов: `track` - трек, `artist` - исполнитель, `playlist` - плейлист, `album` - альбом.

            Идентификатор плейлиста указывается в формате `playlist_id:owner_id`. Где `playlist_id` - идентификатор
            плейлиста, `owner_id` - уникальный идентификатор владельца плейлиста.

        Args:
            object_type (:obj:`str`): Тип объекта.
            ids (:obj:`str` | :obj:`int` | :obj:`list` из :obj:`str` | :obj:`list` из :obj:`int`): Уникальный
                идентификатор объекта или объектов.
            remove (:obj:`bool`, optional): Если :obj:`True` то снимает отметку, иначе ставит.
            user_id (:obj:`str` | :obj:`int`, optional): Уникальный идентификатор пользователя. Если не указан
                используется ID текущего пользователя.
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`bool`: :obj:`True` при успешном выполнении запроса, иначе :obj:`False`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        if user_id is None and self.me is not None:
            user_id = self.me.account.uid

        action = 'remove' if remove else 'add-multiple'
        url = f'{self.base_url}/users/{user_id}/likes/{object_type}s/{action}'

        result = self._request.post(url, {f'{object_type}-ids': ids}, timeout=timeout, *args, **kwargs)

        if object_type == 'track':
            return 'revision' in result

        return result == 'ok'

    @log
    def users_likes_tracks_add(self, track_ids: Union[List[Union[str, int]], str, int], user_id: Union[str, int] = None,
                               timeout: Union[int, float] = None, *args, **kwargs) -> bool:
        """Поставить отметку "Мне нравится" треку/трекам.

        Note:
            Так же снимает отметку "Не рекомендовать" если она есть.

        Args:
            track_ids (:obj:`str` | :obj:`int` | :obj:`list` из :obj:`str` | :obj:`list` из :obj:`int`): Уникальный
                идентификатор трека или треков.
            user_id (:obj:`str` | :obj:`int`, optional): Уникальный идентификатор пользователя. Если не указан
                используется ID текущего пользователя.
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`bool`: :obj:`True` при успешном выполнении запроса, иначе :obj:`False`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        return self._like_action('track', track_ids, False, user_id, timeout, *args, **kwargs)

    @log
    def users_likes_tracks_remove(self, track_ids: Union[List[Union[str, int]], str, int],
                                  user_id: Union[str, int] = None,
                                  timeout: Union[int, float] = None, *args, **kwargs) -> bool:
        """Снять отметку "Мне нравится" у трека/треков.

        Args:
            track_ids (:obj:`str` | :obj:`int` | :obj:`list` из :obj:`str` | :obj:`list` из :obj:`int`): Уникальный
                идентификатор трека или треков.
            user_id (:obj:`str` | :obj:`int`, optional): Уникальный идентификатор пользователя. Если не указан
                используется ID текущего пользователя.
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`bool`: :obj:`True` при успешном выполнении запроса, иначе :obj:`False`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        return self._like_action('track', track_ids, True, user_id, timeout, *args, **kwargs)

    @log
    def users_likes_artists_add(self, artist_ids: Union[List[Union[str, int]], str, int],
                                user_id: Union[str, int] = None,
                                timeout: Union[int, float] = None, *args, **kwargs) -> bool:
        """Поставить отметку "Мне нравится" исполнителю/исполнителям.

        Args:
            artist_ids (:obj:`str` | :obj:`int` | :obj:`list` из :obj:`str` | :obj:`list` из :obj:`int`): Уникальный
                идентификатор артиста или артистов.
            user_id (:obj:`str` | :obj:`int`, optional): Уникальный идентификатор пользователя. Если не указан
                используется ID текущего пользователя.
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`bool`: :obj:`True` при успешном выполнении запроса, иначе :obj:`False`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        return self._like_action('artist', artist_ids, False, user_id, timeout, *args, **kwargs)

    def users_likes_artists_remove(self, artist_ids: Union[List[Union[str, int]], str, int],
                                   user_id: Union[str, int] = None,
                                   timeout: Union[int, float] = None, *args, **kwargs) -> bool:
        """Снять отметку "Мне нравится" у исполнителя/исполнителей.

        Args:
            artist_ids (:obj:`str` | :obj:`int` | :obj:`list` из :obj:`str` | :obj:`list` из :obj:`int`): Уникальный
                идентификатор артиста или артистов.
            user_id (:obj:`str` | :obj:`int`, optional): Уникальный идентификатор пользователя. Если не указан
                используется ID текущего пользователя.
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`bool`: :obj:`True` при успешном выполнении запроса, иначе :obj:`False`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        return self._like_action('artist', artist_ids, True, user_id, timeout, *args, **kwargs)

    @log
    def users_likes_playlists_add(self, playlist_ids: Union[List[Union[str, int]], str, int],
                                  user_id: Union[str, int] = None,
                                  timeout: Union[int, float] = None, *args, **kwargs) -> bool:
        """Поставить отметку "Мне нравится" плейлисту/плейлистам.

        Note:
            Идентификатор плейлиста указывается в формате `playlist_id:owner_id`. Где `playlist_id` - идентификатор
            плейлиста, `owner_id` - уникальный идентификатор владельца плейлиста.

        Args:
            playlist_ids (:obj:`str` | :obj:`int` | :obj:`list` из :obj:`str` | :obj:`list` из :obj:`int`): Уникальный
                идентификатор плейлиста или плейлистов.
            user_id (:obj:`str` | :obj:`int`, optional): Уникальный идентификатор пользователя. Если не указан
                используется ID текущего пользователя.
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`bool`: :obj:`True` при успешном выполнении запроса, иначе :obj:`False`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        return self._like_action('playlist', playlist_ids, False, user_id, timeout, *args, **kwargs)

    @log
    def users_likes_playlists_remove(self, playlist_ids: Union[List[Union[str, int]], str, int],
                                     user_id: Union[str, int] = None,
                                     timeout: Union[int, float] = None, *args, **kwargs) -> bool:
        """Снять отметку "Мне нравится" у плейлиста/плейлистов.

        Note:
            Идентификатор плейлиста указывается в формате `playlist_id:owner_id`. Где `playlist_id` - идентификатор
            плейлиста, `owner_id` - уникальный идентификатор владельца плейлиста.

        Args:
            playlist_ids (:obj:`str` | :obj:`int` | :obj:`list` из :obj:`str` | :obj:`list` из :obj:`int`): Уникальный
                идентификатор плейлиста или плейлистов.
            user_id (:obj:`str` | :obj:`int`, optional): Уникальный идентификатор пользователя. Если не указан
                используется ID текущего пользователя.
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`bool`: :obj:`True` при успешном выполнении запроса, иначе :obj:`False`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        return self._like_action('playlist', playlist_ids, True, user_id, timeout, *args, **kwargs)

    @log
    def users_likes_albums_add(self, album_ids: Union[List[Union[str, int]], str, int], user_id: Union[str, int] = None,
                               timeout: Union[int, float] = None, *args, **kwargs) -> bool:
        """Поставить отметку "Мне нравится" альбому/альбомам.

        Args:
            album_ids (:obj:`str` | :obj:`int` | :obj:`list` из :obj:`str` | :obj:`list` из :obj:`int`): Уникальный
                идентификатор артиста или артистов.
            user_id (:obj:`str` | :obj:`int`, optional): Уникальный идентификатор пользователя. Если не указан
                используется ID текущего пользователя.
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`bool`: :obj:`True` при успешном выполнении запроса, иначе :obj:`False`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        return self._like_action('album', album_ids, False, user_id, timeout, *args, **kwargs)

    @log
    def users_likes_albums_remove(self, album_ids: Union[List[Union[str, int]], str, int],
                                  user_id: Union[str, int] = None,
                                  timeout: Union[int, float] = None, *args, **kwargs) -> bool:
        """Снять отметку "Мне нравится" у альбома/альбомов.

        Args:
            album_ids (:obj:`str` | :obj:`int` | :obj:`list` из :obj:`str` | :obj:`list` из :obj:`int`): Уникальный
                идентификатор артиста или артистов.
            user_id (:obj:`str` | :obj:`int`, optional): Уникальный идентификатор пользователя. Если не указан
                используется ID текущего пользователя.
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`bool`: :obj:`True` при успешном выполнении запроса, иначе :obj:`False`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        return self._like_action('album', album_ids, True, user_id, timeout, *args, **kwargs)

    def _get_list(self, object_type: str, ids: Union[List[Union[str, int]], int, str],
                  params: dict = None, timeout: Union[int, float] = None,
                  *args, **kwargs) -> List[Union[Artist, Album, Track, Playlist]]:
        """Получение объекта/объектов.

        Args:
            object_type (:obj:`str`): Тип объекта.
            ids (:obj:`str` | :obj:`int` | :obj:`list` из :obj:`str` | :obj:`list` из :obj:`int`): Уникальный
                идентификатор объекта или объектов.
            params (:obj:`dict`, optional): Параметры, которые будут переданы в запрос.
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

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

        result = self._request.post(url, params, timeout=timeout, *args, **kwargs)

        return de_list.get(object_type)(result, self)

    @log
    def artists(self, artist_ids: Union[List[Union[str, int]], int, str], timeout: Union[int, float] = None,
                *args, **kwargs) -> List[Artist]:
        """Получение исполнителя/исполнителей.

        Args:
            artist_ids (:obj:`str` | :obj:`int` | :obj:`list` из :obj:`str` | :obj:`list` из :obj:`int`): Уникальный
                идентификатор исполнителя или исполнителей.
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`list` из :obj:`yandex_music.Artist`: Исполнитель или исполнители.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        return self._get_list('artist', artist_ids, timeout=timeout, *args, **kwargs)

    @log
    def albums(self, album_ids: Union[List[Union[str, int]], int, str], timeout: Union[int, float] = None,
               *args, **kwargs) -> List[Album]:
        """Получение альбома/альбомов.

        Args:
            album_ids (:obj:`str` | :obj:`int` | :obj:`list` из :obj:`str` | :obj:`list` из :obj:`int`): Уникальный
                идентификатор альбома или альбомов.
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`list` из :obj:`yandex_music.Album`: Альбом или альбомы.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        return self._get_list('album', album_ids, timeout=timeout, *args, **kwargs)

    @log
    def tracks(self, track_ids: Union[List[Union[str, int]], int, str], with_positions: bool = True,
               timeout: Union[int, float] = None, *args, **kwargs) -> List[Track]:
        """Получение трека/треков.

        Args:
            track_ids (:obj:`str` | :obj:`int` | :obj:`list` из :obj:`str` | :obj:`list` из :obj:`int`): Уникальный
                идентификатор трека или треков.
            with_positions (:obj:`bool`, optional): С позициями TODO.
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`list` из :obj:`yandex_music.Track`: Трек или Треки.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        return self._get_list('track', track_ids, {'with-positions': with_positions}, timeout, *args, **kwargs)

    @log
    def playlists_list(self, playlist_ids: Union[List[Union[str, int]], int, str], timeout: Union[int, float] = None,
                       *args, **kwargs) -> List[Playlist]:
        """Получение плейлиста/плейлистов.

        Note:
            Идентификатор плейлиста указывается в формате `playlist_id:owner_id`. Где `playlist_id` - идентификатор
            плейлиста, `owner_id` - уникальный идентификатор владельца плейлиста.

        Args:
            playlist_ids (:obj:`str` | :obj:`int` | :obj:`list` из :obj:`str` | :obj:`list` из :obj:`int`): Уникальный
                идентификатор плейлиста или плейлистов.
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`list` из :obj:`yandex_music.Playlist`: Плейлист или плейлисты.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        return self._get_list('playlist', playlist_ids, timeout=timeout, *args, **kwargs)

    @log
    def users_playlists_list(self, user_id: Union[str, int] = None, timeout: Union[int, float] = None,
                             *args, **kwargs) -> List[Playlist]:
        """Получение списка плейлистов пользователя.

        Args:
            user_id (:obj:`str` | :obj:`int`, optional): Уникальный идентификатор пользователя. Если не указан
                используется ID текущего пользователя.
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`list` из :obj:`yandex_music.Playlist`: Плейлисты пользователя.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        if user_id is None and self.me is not None:
            user_id = self.me.account.uid

        url = f'{self.base_url}/users/{user_id}/playlists/list'

        result = self._request.get(url, timeout=timeout, *args, **kwargs)

        return Playlist.de_list(result, self)

    def _get_likes(self, object_type: str, user_id: Union[str, int] = None, params: dict = None,
                   timeout: Union[int, float] = None, *args, **kwargs) -> Union[List[Like], Optional[TracksList]]:
        """Получение объектов с отметкой "Мне нравится".

        Args:
            object_type (:obj:`str`): Тип объекта.
            user_id (:obj:`str` | :obj:`int`, optional): Уникальный идентификатор пользователя. Если не указан
                используется ID текущего пользователя.
            params (:obj:`dict`, optional): Параметры, которые будут переданы в запрос.
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`list` из :obj:`yandex_music.Like` | :obj:`yandex_music.TracksList`: Объекты с отметкой "Мне нравится".

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        if user_id is None and self.me is not None:
            user_id = self.me.account.uid

        url = f'{self.base_url}/users/{user_id}/likes/{object_type}s'

        result = self._request.get(url, params, timeout=timeout, *args, **kwargs)

        if object_type == 'track':
            return TracksList.de_json(result.get('library'), self)

        return Like.de_list(result, self, object_type)

    @log
    def users_likes_tracks(self, user_id: Union[str, int] = None, if_modified_since_revision: int = 0,
                           timeout: Union[int, float] = None, *args, **kwargs) -> Optional[TracksList]:
        """Получение треков с отметкой "Мне нравится".

        Args:
            user_id (:obj:`str` | :obj:`int`, optional): Уникальный идентификатор пользователя. Если не указан
                используется ID текущего пользователя.
            if_modified_since_revision (:obj:`int`, optional): TODO.
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.TracksList`: Треки с отметкой "Мне нравится".

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        return self._get_likes('track', user_id, {'if-modified-since-revision': if_modified_since_revision}, timeout,
                               *args, **kwargs)

    @log
    def users_likes_albums(self, user_id: Union[str, int] = None, rich: bool = True, timeout: Union[int, float] = None,
                           *args, **kwargs) -> List[Like]:
        """Получение альбомов с отметкой "Мне нравится".

        Args:
            user_id (:obj:`str` | :obj:`int`, optional): Уникальный идентификатор пользователя. Если не указан
                используется ID текущего пользователя.
            rich (:obj:`bool`, optional): Если False, то приходит укороченная версия.
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`list` из :obj:`yandex_music.Like`: Альбомы с отметкой "Мне нравится".

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        return self._get_likes('album', user_id, {'rich': rich}, timeout, *args, **kwargs)

    @log
    def users_likes_artists(self, user_id: Union[str, int] = None, with_timestamps: bool = True,
                            timeout: Union[int, float] = None, *args, **kwargs) -> List[Like]:
        """Получение артистов с отметкой "Мне нравится".

        Args:
            user_id (:obj:`str` | :obj:`int`, optional): Уникальный идентификатор пользователя. Если не указан
                используется ID текущего пользователя.
            with_timestamps (:obj:`bool`, optional):  С временными метками TODO.
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`list` из :obj:`yandex_music.Like`: Артисты с отметкой "Мне нравится".

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        return self._get_likes('artist', user_id, {'with-timestamps': with_timestamps}, timeout, *args, **kwargs)

    @log
    def users_likes_playlists(self, user_id: Union[str, int] = None, timeout: Union[int, float] = None,
                              *args, **kwargs) -> List[Like]:
        """Получение артистов с отметкой "Мне нравится".

        Args:
            user_id (:obj:`str` | :obj:`int`, optional): Уникальный идентификатор пользователя. Если не указан
                используется ID текущего пользователя.
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`list` из :obj:`yandex_music.Like`: Плейлисты с отметкой "Мне нравится".

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        return self._get_likes('playlist', user_id, timeout=timeout, *args, **kwargs)

    @log
    def users_dislikes_tracks(self, user_id: Union[str, int] = None, if_modified_since_revision: int = 0,
                              timeout: Union[int, float] = None, *args, **kwargs) -> Optional[TracksList]:
        """Получение треков с отметкой "Не рекомендовать".

        Args:
            user_id (:obj:`str` | :obj:`int`, optional): Уникальный идентификатор пользователя. Если не указан
                используется ID текущего пользователя.
            if_modified_since_revision (:obj:`bool`, optional): TODO.
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`list` из :obj:`yandex_music.TracksList`: Треки с отметкой "Не рекомендовать".

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        if user_id is None and self.me is not None:
            user_id = self.me.account.uid

        url = f'{self.base_url}/users/{user_id}/dislikes/tracks'

        result = self._request.get(url, {'if_modified_since_revision': if_modified_since_revision},
                                   timeout=timeout, *args, **kwargs)

        return TracksList.de_json(result.get('library'), self)

    def _dislike_action(self, ids: Union[List[Union[str, int]], str, int], remove: bool = False,
                        user_id: Union[str, int] = None, timeout: Union[int, float] = None, *args, **kwargs) -> bool:
        """Действия с отметкой "Не рекомендовать".

        Args:
            ids (:obj:`str` | :obj:`int` | :obj:`list` из :obj:`str` | :obj:`list` из :obj:`int`): Уникальный
                идентификатор объекта или объектов.
            remove (:obj:`bool`, optional): Если :obj:`True`, то снимает отметку, иначе ставит.
            user_id (:obj:`str` | :obj:`int`, optional): Уникальный идентификатор пользователя. Если не указан
                используется ID текущего пользователя.
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`bool`: :obj:`True` при успешном выполнении запроса, иначе :obj:`False`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        if user_id is None and self.me is not None:
            user_id = self.me.account.uid

        action = 'remove' if remove else 'add-multiple'
        url = f'{self.base_url}/users/{user_id}/dislikes/tracks/{action}'

        result = self._request.post(url, {f'track-ids': ids}, timeout=timeout, *args, **kwargs)

        return 'revision' in result

    @log
    def users_dislikes_tracks_add(self, track_ids: Union[List[Union[str, int]], str, int],
                                  user_id: Union[str, int] = None,
                                  timeout: Union[int, float] = None, *args, **kwargs) -> bool:
        """Поставить отметку "Не рекомендовать" треку/трекам.

        Note:
            Так же снимает отметку "Мне нравится" если она есть.

        Args:
            track_ids (:obj:`str` | :obj:`int` | :obj:`list` из :obj:`str` | :obj:`list` из :obj:`int`): Уникальный
                идентификатор трека или треков.
            user_id (:obj:`str` | :obj:`int`, optional): Уникальный идентификатор пользователя. Если не указан
                используется ID текущего пользователя.
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`bool`: :obj:`True` при успешном выполнении запроса, иначе :obj:`False`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        return self._dislike_action(track_ids, False, user_id, timeout, *args, **kwargs)

    @log
    def users_dislikes_tracks_remove(self, track_ids: Union[List[Union[str, int]], str, int],
                                     user_id: Union[str, int] = None,
                                     timeout: Union[int, float] = None, *args, **kwargs) -> bool:
        """Снять отметку "Не рекомендовать" у трека/треков.

        Args:
            track_ids (:obj:`str` | :obj:`int` | :obj:`list` из :obj:`str` | :obj:`list` из :obj:`int`): Уникальный
                идентификатор трека или треков.
            user_id (:obj:`str` | :obj:`int`, optional): Уникальный идентификатор пользователя. Если не указан
                используется ID текущего пользователя.
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

        Returns:
            :obj:`bool`: :obj:`True` при успешном выполнении запроса, иначе :obj:`False`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        return self._dislike_action(track_ids, True, user_id, timeout, *args, **kwargs)

    @log
    def after_track(self, next_track_id: Union[str, int], context_item: str, prev_track_id: Union[str, int] = None,
                    context: str = 'playlist', types: str = 'shot', from_: str = 'mobile-landing-origin-default',
                    timeout: Union[int, float] = None, *args, **kwargs) -> Optional[ShotEvent]:
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
            timeout (:obj:`int` | :obj:`float`, optional): Если это значение указано, используется как время ожидания
                ответа от сервера вместо указанного при создании пула.
            **kwargs (:obj:`dict`, optional): Произвольные аргументы (будут переданы в запрос).

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

        result = self._request.get(url, params=params, timeout=timeout, *args, **kwargs)

        # TODO судя по всему эндпоинт ещё возвращает рекламу после треков для пользователей без подписки.
        return ShotEvent.de_json(result.get('shot_event'), self)

    # camelCase псевдонимы

    #: Псевдоним для :attr:`from_credentials`
    fromCredentials = from_credentials
    #: Псевдоним для :attr:`from_token`
    fromToken = from_token
    #: Псевдоним для :attr:`generate_token_by_username_and_password`
    generateTokenByUsernameAndPassword = generate_token_by_username_and_password
    #: Псевдоним для :attr:`account_status`
    accountStatus = account_status
    #: Псевдоним для :attr:`permission_alerts`
    permissionAlerts = permission_alerts
    #: Псевдоним для :attr:`account_experiments`
    accountExperiments = account_experiments
    #: Псевдоним для :attr:`consume_promo_code`
    consumePromoCode = consume_promo_code
    #: Псевдоним для :attr:`feed_wizard_is_passed`
    feedWizardIsPassed = feed_wizard_is_passed
    #: Псевдоним для :attr:`tracks_download_info`
    tracksDownloadInfo = tracks_download_info
    #: Псевдоним для :attr:`track_supplement`
    trackSupplement = track_supplement
    #: Псевдоним для :attr:`tracks_similar`
    tracksSimilar = tracks_similar
    #: Псевдоним для :attr:`play_audio`
    playAudio = play_audio
    #: Псевдоним для :attr:`albums_with_tracks`
    albumsWithTracks = albums_with_tracks
    #: Псевдоним для :attr:`search_suggest`
    searchSuggest = search_suggest
    #: Псевдоним для :attr:`users_playlists`
    usersPlaylists = users_playlists
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
    #: Псевдоним для :attr:`rotor_account_status`
    rotorAccountStatus = rotor_account_status
    #: Псевдоним для :attr:`rotor_stations_dashboard`
    rotorStationsDashboard = rotor_stations_dashboard
    #: Псевдоним для :attr:`rotor_stations_list`
    rotorStationsList = rotor_stations_list
    #: Псевдоним для :attr:`rotor_station_feedback`
    rotorStationFeedback = rotor_station_feedback
    #: Псевдоним для :attr:`rotor_station_feedback_radio_started`
    rotorStationFeedbackRadioStarted = rotor_station_feedback_radio_started
    #: Псевдоним для :attr:`rotor_station_feedback_track_started`
    rotorStationFeedbackTrackStarted = rotor_station_feedback_track_started
    #: Псевдоним для :attr:`rotor_station_feedback_track_finished`
    rotorStationFeedbackTrackFinished = rotor_station_feedback_track_finished
    #: Псевдоним для :attr:`rotor_station_feedback_skip`
    rotorStationFeedbackSkip = rotor_station_feedback_skip
    #: Псевдоним для :attr:`rotor_station_info`
    rotorStationInfo = rotor_station_info
    #: Псевдоним для :attr:`rotor_station_settings2`
    rotorStationSettings2 = rotor_station_settings2
    #: Псевдоним для :attr:`rotor_station_tracks`
    rotorStationTracks = rotor_station_tracks
    #: Псевдоним для :attr:`artists_brief_info`
    artistsBriefInfo = artists_brief_info
    #: Псевдоним для :attr:`artists_tracks`
    artistsTracks = artists_tracks
    #: Псевдоним для :attr:`artists_direct_albums`
    artistsDirectAlbums = artists_direct_albums
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
    #: Псевдоним для :attr:`playlists_list`
    playlistsList = playlists_list
    #: Псевдоним для :attr:`users_playlists_list`
    usersPlaylistsList = users_playlists_list
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
    #: Псевдоним для :attr:`after_track`
    afterTrack = after_track
