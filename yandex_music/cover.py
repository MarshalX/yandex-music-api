from yandex_music import YandexMusicObject


class Cover(YandexMusicObject):
    def __init__(self,
                 type,
                 prefix,
                 uri,
                 client=None,
                 **kwargs):
        self.type = type
        self.prefix = prefix
        self.uri = uri

        self.client = client

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(Cover, cls).de_json(data, client)

        return cls(client=client, **data)
