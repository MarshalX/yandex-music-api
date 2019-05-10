import logging

from yandex_music import YandexMusicObject, Status, Settings, PermissionAlerts, Experiments
from yandex_music.utils.request import Request
from yandex_music.error import InvalidToken


class Client(YandexMusicObject):
    def __init__(self, token, base_url=None, request=None):
        self.token = token
        self._request = request or Request(token)
        self.logger = logging.getLogger(__name__)

        if base_url is None:
            base_url = 'https://api.music.yandex.net'

        self.base_url = base_url

    @staticmethod
    def _validate_token(token):
        if any(x.isspace() for x in token):
            raise InvalidToken()

        if len(token) != 39:
            raise InvalidToken()

        return token

    @property
    def request(self):
        return self._request

    def status(self, timeout=None, **kwargs):
        url = f'{self.base_url}/account/status'

        result = self._request.get(url, timeout=timeout)

        status = Status.de_json(result, self)

        return status

    def settings(self, timeout=None, **kwargs):
        url = f'{self.base_url}/settings'

        result = self._request.get(url, timeout=timeout)

        settings = Settings.de_json(result, self)

        return settings

    def permission_alerts(self, timeout=None, **kwargs):
        url = f'{self.base_url}/permission-alerts'

        result = self._request.get(url, timeout=timeout)

        permission_alerts = PermissionAlerts.de_json(result, self)

        return permission_alerts

    def experiments(self, timeout=None, **kwargs):
        url = f'{self.base_url}/account/experiments'

        result = self._request.get(url, timeout=timeout)

        experiments = Experiments.de_json(result, self)

        return experiments
