from yandex_music import YandexMusicObject


class MixLink(YandexMusicObject):
    def __init__(self,
                 title,
                 url,
                 url_scheme,
                 text_color,
                 background_color,
                 background_image_uri,
                 cover_white,
                 client=None,
                 **kwargs):
        self.title = title
        self.url = url
        self.url_scheme = url_scheme
        self.text_color = text_color
        self.background_color = background_color
        self.background_image_uri = background_image_uri
        self.cover_white = cover_white

        self.client = client

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(MixLink, cls).de_json(data, client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data, client):
        if not data:
            return []

        mix_links = list()
        for mix_link in data:
            mix_links.append(cls.de_json(mix_link, client))

        return mix_links
