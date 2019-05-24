from yandex_music import YandexMusicObject


class Chart(YandexMusicObject):
    def __init__(self,
                 position,
                 progress,
                 listeners,
                 shift,
                 client=None,
                 **kwargs):
        self.position = position
        self.progress = progress
        self.listeners = listeners
        self.shift = shift

        self.client = client

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(Chart, cls).de_json(data, client)

        return cls(client=client, **data)
