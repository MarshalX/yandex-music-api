"""Основа HTTP-клиентов: общие таймауты, заголовки, обработка ответов."""

import logging
from typing import TYPE_CHECKING, Any, Dict, NoReturn, Optional, Union

from yandex_music.exceptions import (
    BadRequestError,
    NetworkError,
    NotFoundError,
    UnauthorizedError,
    YandexMusicError,
)
from yandex_music.utils.json_compat import loads as _json_loads
from yandex_music.utils.normalize import _convert_camel_to_snake
from yandex_music.utils.response import Response

if TYPE_CHECKING:
    from yandex_music import ClientType


USER_AGENT = 'Yandex-Music-API'
HEADERS = {
    'X-Yandex-Music-Client': 'YandexMusicAndroid/24023621',
}
DEFAULT_TIMEOUT = 5

logging.getLogger('urllib3').setLevel(logging.WARNING)


class DefaultTimeout:
    """Заглушка для установки времени ожидания по умолчанию."""


default_timeout = DefaultTimeout()
TimeoutType = Union[int, float, DefaultTimeout]


class RequestBase:
    """Базовый класс для выполнения запросов.

    Предоставляет общую логику для синхронного и асинхронного классов запросов:
    настройка заголовков, авторизация, парсинг ответов, нормализация ключей.

    Args:
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        headers (:obj:`dict`, optional): Заголовки передаваемые с каждым запросом.
        proxy_url (:obj:`str`, optional): Прокси.
    """

    def __init__(
        self,
        client: Optional['ClientType'] = None,
        headers: Optional[Dict[str, str]] = None,
        proxy_url: Optional[str] = None,
        timeout: 'TimeoutType' = default_timeout,
    ) -> None:
        self.headers = headers or HEADERS.copy()

        self._timeout = DEFAULT_TIMEOUT
        self.set_timeout(timeout)

        if client:
            self.client = self.set_and_return_client(client)

        # aiohttp
        self.proxy_url = proxy_url

        # requests
        self.proxies = {'http': proxy_url, 'https': proxy_url} if proxy_url else None

    def set_language(self, lang: str) -> None:
        """Добавляет заголовок языка для каждого запроса.

        Note:
            Возможные значения `lang`: en/uz/uk/us/ru/kk/hy.

        Args:
            lang (:obj:`str`): Язык.
        """
        self.headers.update({'Accept-Language': lang})

    def set_timeout(self, timeout: Union[int, float, object] = default_timeout) -> None:
        """Устанавливает время ожидания для всех запросов.

        Args:
            timeout (:obj:`int` | :obj:`float`): Время ожидания от сервера.
        """
        self._timeout = timeout
        if isinstance(timeout, DefaultTimeout):
            self._timeout = DEFAULT_TIMEOUT

    def set_authorization(self, token: str) -> None:
        """Добавляет заголовок авторизации для каждого запроса.

        Note:
            Используется при передаче своего экземпляра Request'a клиенту.

        Args:
            token (:obj:`str`): OAuth токен.
        """
        self.headers.update({'Authorization': f'OAuth {token}'})

    def set_and_return_client(self, client: 'ClientType') -> 'ClientType':
        """Принимает клиент и присваивает его текущему объекту. При наличии авторизации добавляет заголовок.

        Args:
            client (:obj:`yandex_music.Client`): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Client`: Клиент Yandex Music.
        """
        self.client = client

        if self.client and self.client.token:
            self.set_authorization(self.client.token)

        return self.client

    @staticmethod
    def _convert_camel_to_snake(text: str) -> str:
        """Конвертация CamelCase в SnakeCase.

        Args:
            text (:obj:`str`): Название переменной в CamelCase.

        Returns:
            :obj:`str`: Название переменной в SnakeCase.
        """
        return _convert_camel_to_snake(text)

    def _parse(self, json_data: bytes) -> Optional[Response]:
        """Разбор ответа от API.

        Note:
            Если данные отсутствуют в ``result``, то переформировывает ответ используя данные из корня.

            Нормализация ключей выполняется лениво: здесь нормализуются только ключи верхнего уровня
            ответа и ключи ``result`` (если это словарь). Более глубокие уровни нормализуются
            в ``cleanup_data`` каждой конкретной модели.

        Args:
            json_data (:obj:`bytes`): Ответ от API.

        Returns:
            :obj:`yandex_music.utils.response.Response`: Ответ API.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        try:
            data = _json_loads(json_data)
        except UnicodeDecodeError as e:
            logging.getLogger(__name__).debug('Logging raw invalid UTF-8 response:\n%r', json_data)
            raise YandexMusicError('Server response could not be decoded using UTF-8') from e
        except (AttributeError, ValueError) as e:
            raise YandexMusicError('Invalid server response') from e

        if isinstance(data, dict) and data.get('result') is None:
            data = {'result': data, 'error': data.get('error'), 'errorDescription': data.get('errorDescription')}

        return Response.de_json(data, self.client)

    def _prepare_kwargs(self, kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """Подготовка аргументов для запроса.

        Args:
            kwargs: Ключевые аргументы запроса.

        Returns:
            :obj:`dict`: Подготовленные аргументы.
        """
        if 'headers' not in kwargs:
            kwargs['headers'] = {}

        kwargs['headers']['User-Agent'] = USER_AGENT

        if isinstance(kwargs['timeout'], DefaultTimeout):
            kwargs['timeout'] = self._timeout

        return kwargs

    def _handle_error_response(self, status_code: int, content: bytes) -> 'NoReturn':
        """Обработка ошибочного ответа от API.

        Args:
            status_code (:obj:`int`): HTTP статус код.
            content (:obj:`bytes`): Тело ответа.

        Raises:
            :class:`yandex_music.exceptions.UnauthorizedError`: При невалидном токене.
            :class:`yandex_music.exceptions.BadRequestError`: При неправильном запросе.
            :class:`yandex_music.exceptions.NotFoundError`: При отсутствии ресурса.
            :class:`yandex_music.exceptions.NetworkError`: При проблемах с сетью.
        """
        message = 'Unknown error'
        try:
            parse = self._parse(content)
            if parse:
                message = parse.get_error()
        except YandexMusicError:
            message = 'Unknown HTTPError'

        if status_code in (401, 403):
            raise UnauthorizedError(message)
        if status_code == 400:
            raise BadRequestError(message)
        if status_code == 404:
            raise NotFoundError(message)
        if status_code in (409, 413):
            raise NetworkError(message)

        if status_code == 502:
            raise NetworkError('Bad Gateway')

        raise NetworkError(f'{message} ({status_code}): {content}')
