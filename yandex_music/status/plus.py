from yandex_music import YandexMusicObject


class Plus(YandexMusicObject):
    def __init__(self,
                 has_plus,
                 is_tutorial_completed,
                 client=None,
                 **kwargs):
        self.has_plus = has_plus
        self.is_tutorial_completed = is_tutorial_completed

        self.client = client

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(Plus, cls).de_json(data, client)

        return cls(client=client, **data)
