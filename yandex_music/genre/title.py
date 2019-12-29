from typing import TYPE_CHECKING, Optional, Dict

if TYPE_CHECKING:
    from yandex_music import Client

from yandex_music import YandexMusicObject


class Title(YandexMusicObject):
    def __init__(self,
                 title: str,
                 full_title: Optional[str] = None,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        self.title = title
        self.full_title = full_title

        self.client = client
        self._id_attrs = (self.title, self.full_title)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Title']:
        if not data:
            return None

        data = super(Title, cls).de_json(data, client)

        return cls(client=client, **data)

    @classmethod
    def de_dict(cls, data, client) -> Dict[str, Optional['Title']]:
        if not data:
            return {}

        titles = dict()
        for lang, title in data.items():
            titles.update({lang: cls.de_json(title, client)})

        return titles
