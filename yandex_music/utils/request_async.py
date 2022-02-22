####################################################################
# THIS IS AUTO GENERATED COPY OF client.py. DON'T EDIT IN BY HANDS #
####################################################################

import re
import logging
import keyword

from typing import TYPE_CHECKING, Optional, Union

# Не используется ujson из-за отсутствия в нём object_hook'a
# Отправка вообще application/x-www-form-urlencoded, а не JSON'a
# https://github.com/psf/requests/blob/master/requests/models.py#L508
import json

import asyncio
import aiohttp
import aiofiles

from yandex_music.utils.response import Response
from yandex_music.exceptions import (
    UnauthorizedError,
    BadRequestError,
    NetworkError,
    YandexMusicError,
    TimedOutError,
    NotFoundError,
)

if TYPE_CHECKING:
    from yandex_music import Client


USER_AGENT = 'Yandex-Music-API'
HEADERS = {
    'X-Yandex-Music-Client': 'YandexMusicAndroid/23020251',
}

reserved_names = keyword.kwlist + ['client']

logging.getLogger('urllib3').setLevel(logging.WARNING)


class Request:
    """Вспомогательный класс для yandex_music, представляющий методы для выполнения POST и GET запросов, скачивания
    файлов.

    Args:
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        headers (:obj:`dict`, optional): Заголовки передаваемые с каждым запросом.
        proxy_url (:obj:`str`, optional): Прокси.
    """

    def __init__(self, client=None, headers=None, proxy_url=None):
        self.headers = headers or HEADERS.copy()

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

    def set_authorization(self, token: str) -> None:
        """Добавляет заголовок авторизации для каждого запроса.

        Note:
            Используется при передаче своего экземпляра Request'a клиенту.

        Args:
            token (:obj:`str`): OAuth токен.
        """
        self.headers.update({'Authorization': f'OAuth {token}'})

    def set_and_return_client(self, client) -> 'Client':
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
    def _object_hook(obj: dict) -> dict:
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
        cleaned_object = {}
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
            decoded_s = json_data.decode('utf-8')
            data = json.loads(decoded_s, object_hook=Request._object_hook)

        except UnicodeDecodeError:
            logging.getLogger(__name__).debug('Logging raw invalid UTF-8 response:\n%r', json_data)
            raise YandexMusicError('Server response could not be decoded using UTF-8')
        except (AttributeError, ValueError):
            raise YandexMusicError('Invalid server response')

        if data.get('result') is None:
            data = {'result': data, 'error': data.get('error'), 'error_description': data.get('error_description')}

        return Response.de_json(data, self.client)

    async def _request_wrapper(self, *args, **kwargs):
        """Обёртка над запросом библиотеки `aiohttp`.

        Note:
            Добавляет необходимые заголовки для запроса, обрабатывает статус коды, следит за таймаутом, кидает
            необходимые исключения, возвращает ответ. Передаёт пользовательские аргументы в запрос.

        Args:
            *args: Произвольные аргументы для `aiohttp.request`.
            **kwargs: Произвольные ключевые аргументы для `aiohttp.request`.

        Returns:
            :obj:`bytes`: Тело ответа.

        Raises:
            :class:`yandex_music.exceptions.TimedOutError`: При превышении времени ожидания.
            :class:`yandex_music.exceptions.UnauthorizedError`: При невалидном токене, долгом ожидании прямой ссылки на файл.
            :class:`yandex_music.exceptions.BadRequestError`: При неправильном запросе.
            :class:`yandex_music.exceptions.NetworkError`: При проблемах с сетью.
        """
        if 'headers' not in kwargs:
            kwargs['headers'] = {}

        kwargs['headers']['User-Agent'] = USER_AGENT

        try:
            async with aiohttp.request(*args, **kwargs) as _resp:
                resp = _resp
                content = await resp.content.read()
        except asyncio.TimeoutError:
            raise TimedOutError()
        except aiohttp.ClientError as e:
            raise NetworkError(e)

        if 200 <= resp.status <= 299:
            return content

        try:
            parse = self._parse(content)
            message = parse.get_error()
        except YandexMusicError:
            message = 'Unknown HTTPError'

        if resp.status in (401, 403):
            raise UnauthorizedError(message)
        elif resp.status == 400:
            raise BadRequestError(message)
        elif resp.status == 404:
            raise NotFoundError(message)
        elif resp.status in (409, 413):
            raise NetworkError(message)

        elif resp.status == 502:
            raise NetworkError('Bad Gateway')
        else:
            raise NetworkError(f'{message} ({resp.status}): {content}')

    async def get(
        self, url: str, params: dict = None, timeout: Union[int, float] = 5, *args, **kwargs
    ) -> Union[dict, str]:
        """Отправка GET запроса.

        Args:
            url (:obj:`str`): Адрес для запроса.
            params (:obj:`str`): GET параметры для запроса.
            timeout (:obj:`int` | :obj:`float`): Используется как время ожидания ответа от сервера вместо указанного
                при создании пула.
            *args: Произвольные аргументы для `aiohttp.request`.
            **kwargs: Произвольные ключевые аргументы для `aiohttp.request`.

        Returns:
            :obj:`dict` | :obj:`str`: Обработанное тело ответа.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        result = await self._request_wrapper(
            'GET',
            url,
            params=params,
            headers=self.headers,
            proxy=self.proxy_url,
            timeout=aiohttp.ClientTimeout(total=timeout),
            *args,
            **kwargs,
        )

        return self._parse(result).get_result()

    async def post(self, url, data=None, timeout=5, *args, **kwargs) -> Union[dict, str]:
        """Отправка POST запроса.

        Args:
            url (:obj:`str`): Адрес для запроса.
            data (:obj:`str`): POST тело запроса.
            timeout (:obj:`int` | :obj:`float`): Используется как время ожидания ответа от сервера вместо указанного
                при создании пула.
            *args: Произвольные аргументы для `aiohttp.request`.
            **kwargs: Произвольные ключевые аргументы для `aiohttp.request`.

        Returns:
            :obj:`dict` | :obj:`str`: Обработанное тело ответа.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        result = await self._request_wrapper(
            'POST',
            url,
            headers=self.headers,
            proxy=self.proxy_url,
            data=data,
            timeout=aiohttp.ClientTimeout(total=timeout),
            *args,
            **kwargs,
        )

        return self._parse(result).get_result()

    async def retrieve(self, url, timeout=5, *args, **kwargs) -> bytes:
        """Отправка GET запроса и получение содержимого без обработки (парсинга).

        Args:
            url (:obj:`str`): Адрес для запроса.
            timeout (:obj:`int` | :obj:`float`): Используется как время ожидания ответа от сервера вместо указанного
                при создании пула.
            *args: Произвольные аргументы для `aiohttp.request`.
            **kwargs: Произвольные ключевые аргументы для `aiohttp.request`.

        Returns:
            :obj:`bytes`: Тело ответа.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        return await self._request_wrapper(
            'GET', url, proxy=self.proxy_url, timeout=aiohttp.ClientTimeout(total=timeout), *args, **kwargs
        )

    async def download(self, url, filename, timeout=5, *args, **kwargs) -> None:
        """Отправка запроса на получение содержимого и его запись в файл.

        Args:
            url (:obj:`str`): Адрес для запроса.
            filename (:obj:`str`): Путь и(или) название файла вместе с расширением.
            timeout (:obj:`int` | :obj:`float`): Используется как время ожидания ответа от сервера вместо указанного
                при создании пула.
            *args: Произвольные аргументы для `aiohttp.request`.
            **kwargs: Произвольные ключевые аргументы для `aiohttp.request`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        result = await self.retrieve(url, timeout=timeout, *args, *kwargs)
        async with aiofiles.open(filename, 'wb') as f:
            await f.write(result)
