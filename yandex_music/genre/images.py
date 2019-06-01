from yandex_music import YandexMusicObject


class Images(YandexMusicObject):
    def __init__(self,
                 _208x208=None,
                 _300x300=None,
                 client=None,
                 **kwargs):
        self._208x208 = _208x208
        self._300x300 = _300x300

        self.client = client

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(Images, cls).de_json(data, client)

        return cls(client=client, **data)

