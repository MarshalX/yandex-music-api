from datetime import datetime

from yandex_music import YandexMusicObject


class Permissions(YandexMusicObject):
    def __init__(self,
                 until,
                 values,
                 default,
                 client=None,
                 **kwargs):
        self.until = datetime.fromisoformat(until)
        self.values = values
        self.default = default

        self.client = client

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(Permissions, cls).de_json(data, client)

        return cls(client=client, **data)
