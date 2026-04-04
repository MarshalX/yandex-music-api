from typing import TYPE_CHECKING, Any, Optional

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
    'DEFAULT_TIMEOUT',
    'HEADERS',
    'USER_AGENT',
    'DefaultTimeout',
    'Request',
    'TimeoutType',
    'default_timeout',
]


class Request(RequestBase):
    """Вспомогательный класс для выполнения запросов.

    Предоставляет методы для выполнения POST и GET запросов, скачивания файлов.

    Args:
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        headers (:obj:`dict`, optional): Заголовки передаваемые с каждым запросом.
        proxy_url (:obj:`str`, optional): Прокси.
    """

    def _request_wrapper(self, *args: Any, **kwargs: Any) -> bytes:
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
        import requests

        kwargs = self._prepare_kwargs(kwargs)

        try:
            resp = requests.request(*args, **kwargs)  # noqa: S113
        except requests.Timeout as e:
            raise TimedOutError from e
        except requests.RequestException as e:
            raise NetworkError(e) from e

        if 200 <= resp.status_code <= 299:
            return resp.content

        self._handle_error_response(resp.status_code, resp.content)
        return None

    def get(
        self, url: str, params: 'JSONType' = None, timeout: 'TimeoutType' = default_timeout, **kwargs: Any
    ) -> Optional['JSONType']:
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

    def post(
        self, url: str, data: 'JSONType', timeout: 'TimeoutType' = default_timeout, **kwargs: Any
    ) -> Optional['JSONType']:
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
