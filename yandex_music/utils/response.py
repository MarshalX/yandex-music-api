from yandex_music import YandexMusicObject


class Response(YandexMusicObject):
    def __init__(self,
                 data,
                 invocation_info=None,
                 result=None,
                 error=None,
                 error_description=None,
                 client=None,
                 **kwargs):
        self.data = data
        self.invocation_info = invocation_info
        self._result = result
        self._error = error
        self.error_description = error_description

        self.client = client

    @property
    def error(self):
        return f'{self._error} {self.error_description if self.error_description else ""}'

    @property
    def result(self):
        return self._result or self.data

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(Response, cls).de_json(data, client)
        data['data'] = data.copy()
        from yandex_music import InvocationInfo
        data['invocation_info'] = InvocationInfo.de_json(data.get('invocation_info'), client)

        return cls(client=client, **data)
