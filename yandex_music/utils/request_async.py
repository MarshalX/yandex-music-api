import asyncio
from typing import TYPE_CHECKING, Any, Dict, Optional

import aiofiles
import aiohttp

from yandex_music.exceptions import NetworkError, TimedOutError
from yandex_music.utils.request_base import (
    DEFAULT_TIMEOUT,
    HEADERS,
    USER_AGENT,
    DefaultTimeout,
    RequestBase,
    TimeoutType,
    default_timeout,
)

if TYPE_CHECKING:
    from yandex_music import JSONType


__all__ = [
    'Request',
    'USER_AGENT',
    'HEADERS',
    'DEFAULT_TIMEOUT',
    'DefaultTimeout',
    'default_timeout',
    'TimeoutType',
]


class Request(RequestBase):
    """Вспомогательный класс для выполнения асинхронных запросов.

    Предоставляет методы для выполнения POST и GET запросов, скачивания файлов.

    Args:
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        headers (:obj:`dict`, optional): Заголовки передаваемые с каждым запросом.
        proxy_url (:obj:`str`, optional): Прокси.
    """

    def _prepare_kwargs(self, kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """Подготовка аргументов для запроса.

        Note:
            Оборачивает timeout в aiohttp.ClientTimeout.

        Args:
            kwargs: Ключевые аргументы запроса.

        Returns:
            :obj:`dict`: Подготовленные аргументы.
        """
        kwargs = super()._prepare_kwargs(kwargs)
        kwargs['timeout'] = aiohttp.ClientTimeout(total=kwargs['timeout'])
        return kwargs

    async def _request_wrapper(self, *args: Any, **kwargs: Any) -> bytes:  # noqa: C901
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
            :class:`yandex_music.exceptions.UnauthorizedError`: При невалидном токене,
                долгом ожидании прямой ссылки на файл.
            :class:`yandex_music.exceptions.BadRequestError`: При неправильном запросе.
            :class:`yandex_music.exceptions.NetworkError`: При проблемах с сетью.
        """
        kwargs = self._prepare_kwargs(kwargs)

        try:
            async with aiohttp.request(*args, **kwargs) as _resp:
                resp = _resp
                content = await resp.content.read()
        except asyncio.TimeoutError as e:
            raise TimedOutError from e
        except aiohttp.ClientError as e:
            raise NetworkError(e) from e

        if 200 <= resp.status <= 299:
            return content

        self._handle_error_response(resp.status, content)
        return None

    async def get(
        self, url: str, params: 'JSONType' = None, timeout: 'TimeoutType' = default_timeout, **kwargs: Any
    ) -> Optional['JSONType']:
        """Отправка GET запроса.

        Args:
            url (:obj:`str`): Адрес для запроса.
            params (:obj:`str`): GET параметры для запроса.
            timeout (:obj:`int` | :obj:`float`): Используется как время ожидания ответа от сервера вместо указанного
                при создании пула.
            **kwargs: Произвольные ключевые аргументы для `aiohttp.request`.

        Returns:
            :obj:`JSONType`: Обработанное тело ответа.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        result = await self._request_wrapper(
            'GET', url, params=params, headers=self.headers, proxy=self.proxy_url, timeout=timeout, **kwargs
        )
        response = self._parse(result)
        if response:
            return response.get_result()

        return None

    async def post(
        self, url: str, data: 'JSONType', timeout: 'TimeoutType' = default_timeout, **kwargs: Any
    ) -> Optional['JSONType']:
        """Отправка POST запроса.

        Args:
            url (:obj:`str`): Адрес для запроса.
            data (:obj:`str`): POST тело запроса.
            timeout (:obj:`int` | :obj:`float`): Используется как время ожидания ответа от сервера вместо указанного
                при создании пула.
            **kwargs: Произвольные ключевые аргументы для `aiohttp.request`.

        Returns:
            :obj:`JSONType`: Обработанное тело ответа.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        result = await self._request_wrapper(
            'POST', url, headers=self.headers, proxy=self.proxy_url, data=data, timeout=timeout, **kwargs
        )
        response = self._parse(result)
        if response:
            return response.get_result()

        return None

    async def retrieve(self, url: str, timeout: 'TimeoutType' = default_timeout, **kwargs: Any) -> bytes:
        """Отправка GET запроса и получение содержимого без обработки (парсинга).

        Args:
            url (:obj:`str`): Адрес для запроса.
            timeout (:obj:`int` | :obj:`float`): Используется как время ожидания ответа от сервера вместо указанного
                при создании пула.
            **kwargs: Произвольные ключевые аргументы для `aiohttp.request`.

        Returns:
            :obj:`bytes`: Тело ответа.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        return await self._request_wrapper('GET', url, proxy=self.proxy_url, timeout=timeout, **kwargs)

    async def download(self, url: str, filename: str, timeout: 'TimeoutType' = default_timeout, **kwargs: Any) -> None:
        """Отправка запроса на получение содержимого и его запись в файл.

        Args:
            url (:obj:`str`): Адрес для запроса.
            filename (:obj:`str`): Путь и(или) название файла вместе с расширением.
            timeout (:obj:`int` | :obj:`float`): Используется как время ожидания ответа от сервера вместо указанного
                при создании пула.
            **kwargs: Произвольные ключевые аргументы для `aiohttp.request`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        result = await self.retrieve(url, timeout=timeout, **kwargs)
        async with aiofiles.open(filename, 'wb') as f:
            await f.write(result)
