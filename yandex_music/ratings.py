from yandex_music import YandexMusicObject


class Ratings(YandexMusicObject):
    def __init__(self,
                 week,
                 month,
                 day=None,
                 client=None,
                 **kwargs):
        self.week = week
        self.month = month

        self.day = day

        self.client = client

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(Ratings, cls).de_json(data, client)

        return cls(client=client, **data)
