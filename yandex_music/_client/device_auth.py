####################################################################################################
# THIS IS AUTO GENERATED COPY OF yandex_music/_client_async/device_auth.py. DON'T EDIT IT BY HANDS #
####################################################################################################

import inspect
import secrets
import string
import time
from typing import TYPE_CHECKING, Awaitable, Callable, Optional, Union

from yandex_music import DeviceCode, OAuthToken
from yandex_music._client import log
from yandex_music._client_base import ClientBase
from yandex_music.exceptions import BadRequestError, DeviceAuthError

if TYPE_CHECKING:
    from yandex_music.utils.request import Request


# Публичные OAuth-креды официального Android-приложения Яндекс.Музыки.
_DEFAULT_CLIENT_ID = '23cabbbdc6cd418abb4b39c32c41195d'
_DEFAULT_CLIENT_SECRET = '53bc75238f0c4d08a118e51fe9203300'  # noqa: S105
_DEFAULT_DEVICE_NAME = 'YandexMusicAPI'
_OAUTH_BASE_URL = 'https://oauth.yandex.ru'


def _rand_device_id() -> str:
    alphanum = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphanum) for _ in range(10))


OnCodeCallback = Callable[[DeviceCode], Union[None, Awaitable[None]]]


class DeviceAuthMixin(ClientBase):
    """OAuth Device Flow.

    Миксин для получения OAuth-токена Яндекса без сторонних инструментов.
    """

    _request: 'Request'

    @log
    def request_device_code(
        self,
        device_id: Optional[str] = None,
        device_name: Optional[str] = None,
        client_id: Optional[str] = None,
    ) -> DeviceCode:
        """Запрос кода устройства для OAuth Device Flow.

        Args:
            device_id (:obj:`str`, optional): Идентификатор устройства.
                По умолчанию — случайная строка из 10 символов.
            device_name (:obj:`str`, optional): Человекочитаемое имя устройства.
                По умолчанию — ``YandexMusicAPI``.
            client_id (:obj:`str`, optional): OAuth client_id.
                По умолчанию — встроенный client_id Android-приложения Яндекс.Музыки.

        Returns:
            :obj:`yandex_music.DeviceCode`: Код устройства.

        Raises:
            :class:`yandex_music.exceptions.DeviceAuthError`: При некорректном ответе сервера.
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        data = {
            'client_id': client_id or _DEFAULT_CLIENT_ID,
            'device_id': device_id or _rand_device_id(),
            'device_name': device_name or _DEFAULT_DEVICE_NAME,
        }
        result = self._request.post(f'{_OAUTH_BASE_URL}/device/code', data)
        code = DeviceCode.de_json(result, self)
        if code is None:
            raise DeviceAuthError('failed to parse device code response')
        return code

    @log
    def poll_device_token(
        self,
        device_code: str,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
    ) -> Optional[OAuthToken]:
        """Однократный опрос статуса подтверждения кода устройства.

        Note:
            Если пользователь ещё не подтвердил вход, возвращает :obj:`None`
            (OAuth ошибка ``authorization_pending``). Для остальных ошибок OAuth
            (``expired_token``, ``access_denied``, ``invalid_client`` и т.д.)
            бросает :class:`yandex_music.exceptions.DeviceAuthError`.

        Args:
            device_code (:obj:`str`): Значение ``device_code`` из :meth:`request_device_code`.
            client_id (:obj:`str`, optional): OAuth client_id.
            client_secret (:obj:`str`, optional): OAuth client_secret.

        Returns:
            :obj:`yandex_music.OAuthToken` | :obj:`None`: OAuth-токен или ``None``,
                если пользователь ещё не подтвердил вход.

        Raises:
            :class:`yandex_music.exceptions.DeviceAuthError`: Ошибка OAuth (кроме pending).
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        data = {
            'grant_type': 'device_code',
            'code': device_code,
            'client_id': client_id or _DEFAULT_CLIENT_ID,
            'client_secret': client_secret or _DEFAULT_CLIENT_SECRET,
        }
        try:
            result = self._request.post(f'{_OAUTH_BASE_URL}/token', data)
        except BadRequestError as e:
            if 'authorization_pending' in str(e):
                return None
            raise DeviceAuthError(str(e)) from e

        return OAuthToken.de_json(result, self)

    @log
    def device_auth(
        self,
        on_code: OnCodeCallback,
        poll_interval: Optional[float] = None,
        timeout: Optional[float] = None,
        should_cancel: Optional[Callable[[], bool]] = None,
        device_id: Optional[str] = None,
        device_name: Optional[str] = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
    ) -> OAuthToken:
        """Блокирующий OAuth Device Flow: получает код, ждёт подтверждения, возвращает токен.

        Note:
            **Метод блокирующий.** Выполнение возвращается только после того, как пользователь
            подтвердит вход на странице Яндекса, истечёт таймаут или ``should_cancel()`` вернёт ``True``.

            После успешного получения токена метод записывает его в ``self.token`` и обновляет
            заголовок ``Authorization`` у текущего HTTP-клиента, поэтому клиент сразу готов к работе.

        Args:
            on_code (:obj:`Callable`): Обязательный коллбек. Вызывается сразу после
                получения :class:`yandex_music.DeviceCode` — чтобы вызывающий код мог
                показать пользователю ``user_code`` и ``verification_url``.
                В асинхронном клиенте допустимо передать корутину.
            poll_interval (:obj:`float`, optional): Интервал опроса токена в секундах.
                По умолчанию — ``code.interval``, рекомендованный сервером.
            timeout (:obj:`float`, optional): Общий таймаут ожидания в секундах.
                По умолчанию — ``code.expires_in``, возвращённый сервером.
            should_cancel (:obj:`Callable`, optional): Коллбек без аргументов, проверяемый
                на каждой итерации. Если вернёт ``True``, метод бросит
                :class:`yandex_music.exceptions.DeviceAuthError`.
            device_id (:obj:`str`, optional): См. :meth:`request_device_code`.
            device_name (:obj:`str`, optional): См. :meth:`request_device_code`.
            client_id (:obj:`str`, optional): OAuth client_id.
            client_secret (:obj:`str`, optional): OAuth client_secret.

        Returns:
            :obj:`yandex_music.OAuthToken`: Полученный OAuth-токен.

        Raises:
            :class:`yandex_music.exceptions.DeviceAuthError`: При таймауте,
                отмене через ``should_cancel`` или не-pending ошибке OAuth.
        """
        code = self.request_device_code(device_id, device_name, client_id)

        cb_result = on_code(code)
        if inspect.isawaitable(cb_result):
            cb_result = cb_result

        interval = poll_interval if poll_interval is not None else code.interval
        total = timeout if timeout is not None else code.expires_in
        deadline = time.monotonic() + total

        while True:
            if should_cancel is not None and should_cancel():
                raise DeviceAuthError('cancelled by caller')

            token = self.poll_device_token(code.device_code, client_id, client_secret)
            if token is not None:
                self.token = token.access_token
                self._request.set_authorization(token.access_token)
                return token

            if time.monotonic() >= deadline:
                raise DeviceAuthError(f'timed out after {total}s waiting for user confirmation')

            time.sleep(interval)
