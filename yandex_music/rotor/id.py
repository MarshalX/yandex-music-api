from yandex_music import YandexMusicObject


class Id(YandexMusicObject):
    def __init__(self,
                 type,
                 tag,
                 client=None,
                 **kwargs):
        self.type = type
        self.tag = tag

        self.client = client

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(Id, cls).de_json(data, client)

        return cls(client=client, **data)
