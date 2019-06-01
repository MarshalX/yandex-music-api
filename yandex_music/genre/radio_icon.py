from yandex_music import YandexMusicObject


class RadioIcon(YandexMusicObject):
    def __init__(self,
                 background_color,
                 image_url,
                 client=None,
                 **kwargs):
        self.background_color = background_color
        self.image_url = image_url

        self.client = client

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(RadioIcon, cls).de_json(data, client)

        return cls(client=client, **data)
