from yandex_music import YandexMusicObject


class Major(YandexMusicObject):
    def __init__(self,
                 id,
                 name,
                 client=None,
                 **kwargs):
        self.id = id
        self.name = name

        self.client = client
        self._id_attrs = (self.id,)

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(Major, cls).de_json(data, client)

        return cls(client=client, **data)
