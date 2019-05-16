from yandex_music import YandexMusicObject


class Response(YandexMusicObject):
    def __init__(self,
                 invocation_info,
                 result=None,
                 error=None,
                 client=None,
                 **kwargs):
        self.invocation_info = invocation_info
        self.result = result
        self.error = error

        self.client = client

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(Response, cls).de_json(data, client)
        from yandex_music import InvocationInfo
        data['invocation_info'] = InvocationInfo.de_json(data.get('invocation_info'), client)

        return cls(client=client, **data)
