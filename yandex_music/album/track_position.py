from yandex_music import YandexMusicObject


class TrackPosition(YandexMusicObject):
    def __init__(self,
                 volume,
                 index,
                 client=None,
                 **kwargs):
        self.volume = volume
        self.index = index

        self.client = client

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(TrackPosition, cls).de_json(data, client)

        return cls(client=client, **data)
