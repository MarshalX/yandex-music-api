from yandex_music import YandexMusicObject


class Experiments(YandexMusicObject):
    def __init__(self,
                 client=None,
                 **kwargs):
        self.__dict__.update(kwargs)

        self.client = client

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(Experiments, cls).de_json(data, client)

        return cls(client=client, **data)
