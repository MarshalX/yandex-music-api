from typing import TYPE_CHECKING, Optional, List

if TYPE_CHECKING:
    from yandex_music import Client

from yandex_music import YandexMusicObject


class Link(YandexMusicObject):
    def __init__(self,
                 title,
                 href,
                 type_,
                 social_network=None,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        self.title = title
        self.href = href
        self.type = type_

        self.social_network = social_network

        self.client = client
        self._id_attrs = (self.title, self.href, self.type)

    @classmethod
    def de_json(cls, data: dict, client: 'Client'):
        if not data:
            return None

        data = super(Link, cls).de_json(data, client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data: dict, client: 'Client'):
        if not data:
            return []

        links = list()
        for link in data:
            links.append(cls.de_json(link, client))

        return links
