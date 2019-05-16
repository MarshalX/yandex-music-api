from yandex_music import YandexMusicObject


class Response(YandexMusicObject):
    def __init__(self,
                 data,
                 invocation_info=None,
                 result=None,
                 error=None,
                 client=None,
                 **kwargs):
        self.data = data
        self.invocation_info = invocation_info
        self._result = result
        self.error = error

        self.client = client

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
