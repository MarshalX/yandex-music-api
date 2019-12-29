from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from yandex_music import Client, Id, Icon, Restrictions

from yandex_music import YandexMusicObject


class Station(YandexMusicObject):
    def __init__(self,
                 id_: Optional['Id'],
                 name: str,
                 icon: Optional['Icon'],
                 mts_icon: Optional['Icon'],
                 geocell_icon: Optional['Icon'],
                 id_for_from: str,
                 restrictions: Optional['Restrictions'],
                 restrictions2: Optional['Restrictions'],
                 parent_id: Optional['Id'] = None,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        self.id = id_
        self.name = name
        self.icon = icon
        self.mts_icon = mts_icon
        self.geocell_icon = geocell_icon
        self.id_for_from = id_for_from
        self.restrictions = restrictions
        self.restrictions2 = restrictions2

        self.parent_id = parent_id

        self.client = client
        self._id_attrs = (self.id, self.name, self.icon, self.mts_icon, self.geocell_icon,
                          self.id_for_from, self.restrictions, self.restrictions2)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Station']:
        if not data:
            return None

        data = super(Station, cls).de_json(data, client)
        from yandex_music import Id, Icon, Restrictions
        data['id_'] = Id.de_json(data.get('id_'), client)
        data['parent_id'] = Id.de_json(data.get('parent_id'), client)
        data['icon'] = Icon.de_json(data.get('icon'), client)
        data['mts_icon'] = Icon.de_json(data.get('mts_icon'), client)
        data['geocell_icon'] = Icon.de_json(data.get('geocell_icon'), client)
        data['restrictions'] = Restrictions.de_json(data.get('restrictions'), client)
        data['restrictions2'] = Restrictions.de_json(data.get('restrictions2'), client)

        return cls(client=client, **data)
