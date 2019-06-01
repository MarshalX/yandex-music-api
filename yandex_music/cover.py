from yandex_music import YandexMusicObject


class Cover(YandexMusicObject):
    def __init__(self,
                 type=None,
                 uri=None,
                 items_uri=None,
                 dir=None,
                 version=None,
                 custom=None,
                 prefix=None,
                 error=None,
                 client=None,
                 **kwargs):
        self.type = type
        self.uri = uri
        self.items_uri = items_uri
        self.prefix = prefix
        self.dir = dir
        self.version = version
        self.custom = custom
        self.error = error

        self.client = client

    def download(self, filename):
        self.client._request.download(self.uri, filename)

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(Cover, cls).de_json(data, client)

        return cls(client=client, **data)
