import re
import logging
import builtins

from typing import TYPE_CHECKING, Optional, Union

# Не используется ujson из-за отсутствия в нём object_hook'a
# Отправка вообще application/x-www-form-urlencoded, а не JSON'a
# https://github.com/psf/requests/blob/master/requests/models.py#L508
import json

import requests

from yandex_music.utils.captcha_response import CaptchaResponse
from yandex_music.utils.response import Response
from yandex_music.exceptions import Unauthorized, BadRequest, NetworkError, YandexMusicError, CaptchaRequired, \
    CaptchaWrong, TimedOut

if TYPE_CHECKING:
    from yandex_music import Client


USER_AGENT = 'Yandex-Music-API'
HEADERS = {
    'X-Yandex-Music-Client': 'YandexMusicAndroid/23020055',
}

reserved_names = [name.lower() for name in dir(builtins)] + ['client']

logging.getLogger('urllib3').setLevel(logging.WARNING)


class Request:
    """Вспомогательный класс для yandex_music, представляющий методы для выполнения POST и GET запросов, скачивания
    файлов.

    Args:
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        headers (:obj:`dict`, optional): Заголовки передаваемые с каждым запросом.
        proxy_url (:obj:`str`, optional): Прокси.
    """

    def __init__(self,
                 client=None,
                 headers=None,
                 proxy_url=None):
        self.headers = headers or HEADERS.copy()

        self.client = self.set_and_return_client(client)

        self.proxies = {'http': proxy_url, 'https': proxy_url} if proxy_url else None

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
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', text)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    @staticmethod
    def _object_hook(obj: dict) -> dict:
        """Нормализация имён переменных пришедших с API.

        Note:
            В названии переменной заменяет "-" на "_", конвертирует в SnakeCase, если название является
            зарезервированным именем или "client" - добавляет "_" в конец. Если название переменной начинается с цифры -
            добавляет в начало "_".

        Args:
            obj (:obj:`dict`): Словарь, где ключ название переменной, а значение - содержимое.

        Returns:
            :obj:`dict`: Тот же словарь, что и на входе, но с нормализованными ключами.
        """
        cleaned_object = {}
        for key, value in obj.items():
            key = Request._convert_camel_to_snake(key.replace('-', '_'))
            if key.lower() in reserved_names:
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
            logging.getLogger(__name__).debug(
                'Logging raw invalid UTF-8 response:\n%r', json_data)
            raise YandexMusicError('Server response could not be decoded using UTF-8')
        except (AttributeError, ValueError):
            raise YandexMusicError('Invalid server response')

        if data.get('result') is None:
            data = {'result': data, 'error': data.get('error'), 'error_description': data.get('error_description')}

        return Response.de_json(data, self.client)

    def _request_wrapper(self, *args, **kwargs):
        """Обёртка над запросом библиотеки `requests`.

        Note:
            Добавляет необходимые заголовки для запроса, обрабатывает статус коды, следит за таймаутом, кидает
            необходимые исключения, возвращает ответ. Передаёт пользовательские аргументы в запрос.

        Args:
            *args: Произвольные аргументы для `requests.request`.
            **kwargs: Произвольные ключевые аргументы для `requests.request`.

        Returns:
            :obj:`yandex_music.utils.response.Response`: Ответ API.

        Raises:
            :class:`yandex_music.exceptions.TimedOut`: При превышении времени ожидания.
            :class:`yandex_music.exceptions.Unauthorized`: При невалидном токене, долгом ожидании прямой ссылки на файл.
            :class:`yandex_music.exceptions.BadRequest`: При неправильном запросе.
            :class:`yandex_music.exceptions.NetworkError`: При проблемах с сетью.
            :class:`yandex_music.exceptions.CaptchaWrong`: При неправильной капче.
            :class:`yandex_music.exceptions.CaptchaRequired`: При необходимости пройти капчу.
        """
        if 'headers' not in kwargs:
            kwargs['headers'] = {}

        kwargs['headers']['User-Agent'] = USER_AGENT

        try:
            resp = requests.request(*args, **kwargs)
        except requests.Timeout:
            raise TimedOut()
        except requests.RequestException as e:
            raise NetworkError(e)

        if 200 <= resp.status_code <= 299:
            return resp

        parse = self._parse(resp.content)
        message = parse.error or 'Unknown HTTPError'

        if 'CAPTCHA' in message:
            exception = CaptchaWrong if 'Wrong' in message else CaptchaRequired
            raise exception(message, CaptchaResponse.de_json(parse.result, self.client))
        elif resp.status_code in (401, 403):
            raise Unauthorized(message)
        elif resp.status_code == 400:
            raise BadRequest(message)
        elif resp.status_code in (404, 409, 413):
            raise NetworkError(message)

        elif resp.status_code == 502:
            raise NetworkError('Bad Gateway')
        else:
            raise NetworkError(f'{message} ({resp.status_code})')

    def get(self, url: str, params: dict = None, timeout: Union[int, float] = 5, *args, **kwargs):
        """Отправка GET запроса.

        Args:
            url (:obj:`str`): Адрес для запроса.
            params (:obj:`str`): GET параметры для запроса.
            timeout (:obj:`int` | :obj:`float`): Используется как время ожидания ответа от сервера вместо указанного
                при создании пула.
            *args: Произвольные аргументы для `requests.request`.
            **kwargs: Произвольные ключевые аргументы для `requests.request`.

        Returns:
            :obj:`yandex_music.utils.response.Response`: Ответ API.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        result = self._request_wrapper('GET', url, params=params, headers=self.headers, proxies=self.proxies,
                                       timeout=timeout, *args, **kwargs)

        return self._parse(result.content).result

    def post(self, url, data=None, timeout=5, *args, **kwargs):
        """Отправка POST запроса.

        Args:
            url (:obj:`str`): Адрес для запроса.
            data (:obj:`str`): POST тело запроса.
            timeout (:obj:`int` | :obj:`float`): Используется как время ожидания ответа от сервера вместо указанного
                при создании пула.
            *args: Произвольные аргументы для `requests.request`.
            **kwargs: Произвольные ключевые аргументы для `requests.request`.

        Returns:
            :obj:`yandex_music.utils.response.Response`: Ответ API.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        result = self._request_wrapper('POST', url, headers=self.headers, proxies=self.proxies, data=data,
                                       timeout=timeout, *args, **kwargs)

        return self._parse(result.content).result

    def retrieve(self, url, timeout=5, *args, **kwargs):
        """Отправка GET запроса и получение содержимого без обработки (парсинга).

        Args:
            url (:obj:`str`): Адрес для запроса.
            timeout (:obj:`int` | :obj:`float`): Используется как время ожидания ответа от сервера вместо указанного
                при создании пула.
            *args: Произвольные аргументы для `requests.request`.
            **kwargs: Произвольные ключевые аргументы для `requests.request`.

        Returns:
            :obj:`Response`: Экземляр объекта ответа библиотеки `requests`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        return self._request_wrapper('GET', url, proxies=self.proxies, timeout=timeout, *args, **kwargs)

    def download(self, url, filename, timeout=5, *args, **kwargs):
        """Отправка запроса на получение содержимого и его запись в файл.

        Args:
            url (:obj:`str`): Адрес для запроса.
            filename (:obj:`str`): Путь и(или) название файла вместе с расширением.
            timeout (:obj:`int` | :obj:`float`): Используется как время ожидания ответа от сервера вместо указанного
                при создании пула.
            *args: Произвольные аргументы для `requests.request`.
            **kwargs: Произвольные ключевые аргументы для `requests.request`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        result = self.retrieve(url, timeout=timeout, *args, *kwargs)
        with open(filename, 'wb') as f:
            f.write(result.content)
