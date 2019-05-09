import re
import json
import logging
import requests

from yandex_music.error import Unauthorized, BadRequest, NetworkError, YandexMusicError


USER_AGENT = 'Yandex-Music-API'
HEADERS = {
    'X-Yandex-Music-Client': 'Yandex-Music-API',
    'User-Agent': 'Yandex-Music-API',
    'Connection': 'Keep-Alive'
}


class Request(object):
    def __init__(self,
                 token,
                 headers=None,
                 proxies=None):

        self.headers = headers or HEADERS
        self.headers.update({'Authorization': f'OAuth {token}'})

        self.proxies = proxies  # TODO

    @staticmethod
    def _convert_camel_to_snake(text):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', text)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    @staticmethod
    def _object_hook(obj):
        cleaned_object = {}
        for key, value in obj.items():
            key = Request._convert_camel_to_snake(key.replace('-', '_'))
            cleaned_object.update({key: value})

        return cleaned_object

    @staticmethod
    def _parse(json_data):
        try:
            decoded_s = json_data.decode('utf-8')
            data = json.loads(decoded_s, object_hook=Request._object_hook)
        except UnicodeDecodeError:
            logging.getLogger(__name__).debug(
                'Logging raw invalid UTF-8 response:\n%r', json_data)
            raise YandexMusicError('Server response could not be decoded using UTF-8')
        except ValueError:
            raise Exception('Invalid server response')

        return data['result']

    def _request_wrapper(self, *args, **kwargs):
        if 'headers' not in kwargs:
            kwargs['headers'] = {}

        kwargs['headers']['user-agent'] = USER_AGENT

        try:
            resp = requests.request(verify=False, *args, **kwargs)
        except requests.Timeout:
            raise TimeoutError()
        except requests.RequestException:
            raise Exception('Network error')

        if 200 <= resp.status_code <= 299:
            return resp.content

        try:
            message = self._parse(resp.text)
        except ValueError:
            message = 'Unknown HTTPError'

        if resp.status_code in (401, 403):
            raise Unauthorized(message)
        elif resp.status_code == 400:
            raise BadRequest(message)
        elif resp.status_code in (404, 409, 413):
            raise NetworkError()

        elif resp.status_code == 502:
            raise NetworkError('Bad Gateway')
        else:
            raise NetworkError('{0} ({1})'.format(message, resp.status_code))

    def get(self, url, timeout=5):
        result = self._request_wrapper('GET', url, headers=self.headers, timeout=timeout)
        return self._parse(result)

    def post(self, url, data, timeout=5):
        result = self._request_wrapper('POST', url, headers=self.headers, data=data, timeout=timeout)
        return self._parse(result)

