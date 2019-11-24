import re
import json
import logging
import requests

from yandex_music.utils.captcha_response import CaptchaResponse
from yandex_music.utils.response import Response
from yandex_music.exceptions import Unauthorized, BadRequest, NetworkError, YandexMusicError, CaptchaRequired, \
    CaptchaWrong

USER_AGENT = 'Yandex-Music-API'
HEADERS = {
    'X-Yandex-Music-Client': 'WindowsPhone/3.20',
}


logging.getLogger('urllib3').setLevel(logging.WARNING)


class Request:
    """Вспомогателньный класс для yandex_music предоставляющий методы для выполнения POST и GET запросов, скачивания
    файлов.

    Args:
        client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
            Music.
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

    def set_authorization(self, token):
        self.headers.update({'Authorization': f'OAuth {token}'})

    def set_and_return_client(self, client):
        self.client = client

        if self.client and self.client.token:
            self.set_authorization(self.client.token)

        return self.client

    @staticmethod
    def _convert_camel_to_snake(text):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', text)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    @staticmethod
    def _object_hook(obj):
        cleaned_object = {}
        for key, value in obj.items():
            key = Request._convert_camel_to_snake(key.replace('-', '_'))
            key = key.replace('client', 'client_')

            if len(key) and key[0].isdigit():
                key = '_' + key

            cleaned_object.update({key: value})

        return cleaned_object

    def _parse(self, json_data) -> Response:
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
        if 'headers' not in kwargs:
            kwargs['headers'] = {}

        kwargs['headers']['User-Agent'] = USER_AGENT

        try:
            resp = requests.request(*args, **kwargs)
        except requests.Timeout:
            raise TimeoutError()
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

    def get(self, url, params=None, timeout=5, *args, **kwargs):
        result = self._request_wrapper('GET', url, params=params, headers=self.headers, proxies=self.proxies,
                                       timeout=timeout, *args, **kwargs)

        return self._parse(result.content).result

    def post(self, url, data=None, timeout=5, *args, **kwargs):
        result = self._request_wrapper('POST', url, headers=self.headers, proxies=self.proxies, data=data,
                                       timeout=timeout, *args, **kwargs)

        return self._parse(result.content).result

    def retrieve(self, url, timeout=5, *args, **kwargs):
        return self._request_wrapper('GET', url, proxies=self.proxies, timeout=timeout, *args, **kwargs)

    def download(self, url, filename, timeout=5, *args, **kwargs):
        result = self.retrieve(url, timeout=timeout, *args, *kwargs)
        with open(filename, 'wb') as f:
            f.write(result.content)
