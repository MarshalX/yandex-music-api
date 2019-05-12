from yandex_music import YandexMusicObject


class PlayCounter(YandexMusicObject):
    def __init__(self,
                 value,
                 description,
                 updated,
                 client=None,
                 **kwargs):
        self.value = value
        self.description = description
        self.updated = updated

        self.client = client

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(PlayCounter, cls).de_json(data, client)

        return cls(client=client, **data)
