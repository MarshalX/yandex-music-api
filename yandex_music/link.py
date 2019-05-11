from yandex_music import YandexMusicObject


class Link(YandexMusicObject):
    def __init__(self,
                 title,
                 href,
                 type,
                 social_network=None,
                 client=None,
                 **kwargs):
        self.title = title
        self.href = href
        self.type = type

        self.social_network = social_network

        self.client = client
        self._id_attrs = (self.href,)

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(Link, cls).de_json(data, client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data, client):
        if not data:
            return []

        links = list()
        for link in data:
            links.append(cls.de_json(link, client))

        return links
