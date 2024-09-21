# Не используется ujson из-за отсутствия в нём object_hook'a
# Отправка вообще application/x-www-form-urlencoded, а не JSON'a
# https://github.com/psf/requests/blob/master/requests/models.py#L508
import json
import keyword
import logging
import re
from typing import TYPE_CHECKING, Any, Dict, Optional, Union

import requests

from yandex_music.exceptions import (
    BadRequestError,
    NetworkError,
    NotFoundError,
    TimedOutError,
    UnauthorizedError,
    YandexMusicError,
)
from yandex_music.utils.response import Response

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType


USER_AGENT = 'Yandex-Music-API'
HEADERS = {
    'X-Yandex-Music-Client': 'YandexMusicAndroid/24023621',
}
DEFAULT_TIMEOUT = 5

reserved_names = list(keyword.kwlist) + ['ClientType']

logging.getLogger('urllib3').setLevel(logging.WARNING)


class DefaultTimeout:
    """Заглушка для установки времени ожидания по умолчанию."""


default_timeout = DefaultTimeout()
TimeoutType = Union[int, float, DefaultTimeout]


class Request:
    """Вспомогательный класс для выполнения запросов.

    Предоставляет методы для выполнения POST и GET запросов, скачивания файлов.

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
        if timeout is default_timeout:
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
        s = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', text)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s).lower()

    @staticmethod
    def _object_hook(obj: 'JSONType') -> 'JSONType':
        """Нормализация имён переменных пришедших с API.

        Note:
            В названии переменной заменяет "-" на "_", конвертирует в SnakeCase, если название является
            зарезервированным словом или "client" - добавляет "_" в конец. Если название переменной начинается с цифры -
            добавляет в начало "_".

        Args:
            obj (:obj:`dict`): Словарь, где ключ название переменной, а значение - содержимое.

        Returns:
            :obj:`dict`: Тот же словарь, что и на входе, но с нормализованными ключами.
        """
        if not isinstance(obj, dict):
            return obj

        cleaned_object: Dict[str, JSONType] = {}
        for key, value in obj.items():
            key = Request._convert_camel_to_snake(key.replace('-', '_'))
            key = key.lower()

            if key in reserved_names:
                key += '_'

            if len(key) and key[0].isdigit():
                key = '_' + key

            cleaned_object.update({key: value})

        return cleaned_object

    def _parse(self, json_data: bytes) -> Optional[Response]:
        """Разбор ответа от API.

        Note:
            Если данные отсутствуют в `result`, то переформировывает ответ используя данные из корня.

        Args:
            json_data (:obj:`bytes`): Ответ от API.

        Returns:
            :obj:`yandex_music.utils.response.Response`: Ответ API.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        try:
            decoded_s = json_data.decode('UTF-8')
            data = json.loads(decoded_s, object_hook=Request._object_hook)

        except UnicodeDecodeError as e:
            logging.getLogger(__name__).debug('Logging raw invalid UTF-8 response:\n%r', json_data)
            raise YandexMusicError('Server response could not be decoded using UTF-8') from e
        except (AttributeError, ValueError) as e:
            raise YandexMusicError('Invalid server response') from e

        if data.get('result') is None:
            data = {'result': data, 'error': data.get('error'), 'error_description': data.get('error_description')}

        return Response.de_json(data, self.client)

    def _request_wrapper(self, *args: Any, **kwargs: Any) -> bytes:  # noqa: C901
        """Обёртка над запросом библиотеки `requests`.

        Note:
            Добавляет необходимые заголовки для запроса, обрабатывает статус коды, следит за таймаутом, кидает
            необходимые исключения, возвращает ответ. Передаёт пользовательские аргументы в запрос.

        Args:
            *args: Произвольные аргументы для `requests.request`.
            **kwargs: Произвольные ключевые аргументы для `requests.request`.

        Returns:
            :obj:`bytes`: Тело ответа.

        Raises:
            :class:`yandex_music.exceptions.TimedOutError`: При превышении времени ожидания.
            :class:`yandex_music.exceptions.UnauthorizedError`: При невалидном токене,
                долгом ожидании прямой ссылки на файл.
            :class:`yandex_music.exceptions.BadRequestError`: При неправильном запросе.
            :class:`yandex_music.exceptions.NetworkError`: При проблемах с сетью.
        """
        if 'headers' not in kwargs:
            kwargs['headers'] = {}

        kwargs['headers']['User-Agent'] = USER_AGENT

        if kwargs['timeout'] is default_timeout:
            kwargs['timeout'] = self._timeout

        try:
            resp = requests.request(*args, **kwargs)
        except requests.Timeout as e:
            raise TimedOutError from e
        except requests.RequestException as e:
            raise NetworkError(e) from e

        if 200 <= resp.status_code <= 299:
            return resp.content

        message = 'Unknown error'
        try:
            parse = self._parse(resp.content)
            if parse:
                message = parse.get_error()
        except YandexMusicError:
            message = 'Unknown HTTPError'

        if resp.status_code in (401, 403):
            raise UnauthorizedError(message)
        if resp.status_code == 400:
            raise BadRequestError(message)
        if resp.status_code == 404:
            raise NotFoundError(message)
        if resp.status_code in (409, 413):
            raise NetworkError(message)

        if resp.status_code == 502:
            raise NetworkError('Bad Gateway')

        raise NetworkError(f'{message} ({resp.status_code}): {resp.content}')

    def get(
        self, url: str, params: 'JSONType' = None, timeout: 'TimeoutType' = default_timeout, **kwargs: Any
    ) -> 'JSONType':
        """Отправка GET запроса.

        Args:
            url (:obj:`str`): Адрес для запроса.
            params (:obj:`str`): GET параметры для запроса.
            timeout (:obj:`int` | :obj:`float`): Используется как время ожидания ответа от сервера вместо указанного
                при создании пула.
            **kwargs: Произвольные ключевые аргументы для `requests.request`.

        Returns:
            :obj:`JSONType`: Обработанное тело ответа.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        result = self._request_wrapper(
            'GET', url, params=params, headers=self.headers, proxies=self.proxies, timeout=timeout, **kwargs
        )
        response = self._parse(result)
        if response:
            return response.get_result()

        return None

    def post(self, url: str, data: 'JSONType', timeout: 'TimeoutType' = default_timeout, **kwargs: Any) -> 'JSONType':
        """Отправка POST запроса.

        Args:
            url (:obj:`str`): Адрес для запроса.
            data (:obj:`str`): POST тело запроса.
            timeout (:obj:`int` | :obj:`float`): Используется как время ожидания ответа от сервера вместо указанного
                при создании пула.
            **kwargs: Произвольные ключевые аргументы для `requests.request`.

        Returns:
            :obj:`JSONType`: Обработанное тело ответа.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        result = self._request_wrapper(
            'POST', url, headers=self.headers, proxies=self.proxies, data=data, timeout=timeout, **kwargs
        )
        response = self._parse(result)
        if response:
            return response.get_result()

        return None

    def retrieve(self, url: str, timeout: 'TimeoutType' = default_timeout, **kwargs: Any) -> bytes:
        """Отправка GET запроса и получение содержимого без обработки (парсинга).

        Args:
            url (:obj:`str`): Адрес для запроса.
            timeout (:obj:`int` | :obj:`float`): Используется как время ожидания ответа от сервера вместо указанного
                при создании пула.
            **kwargs: Произвольные ключевые аргументы для `requests.request`.

        Returns:
            :obj:`bytes`: Тело ответа.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        return self._request_wrapper('GET', url, proxies=self.proxies, timeout=timeout, **kwargs)

    def download(self, url: str, filename: str, timeout: 'TimeoutType' = default_timeout, **kwargs: Any) -> None:
        """Отправка запроса на получение содержимого и его запись в файл.

        Args:
            url (:obj:`str`): Адрес для запроса.
            filename (:obj:`str`): Путь и(или) название файла вместе с расширением.
            timeout (:obj:`int` | :obj:`float`): Используется как время ожидания ответа от сервера вместо указанного
                при создании пула.
            **kwargs: Произвольные ключевые аргументы для `requests.request`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        result = self.retrieve(url, timeout=timeout, **kwargs)
        with open(filename, 'wb') as f:
            f.write(result)
