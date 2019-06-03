from yandex_music import YandexMusicObject


class Station(YandexMusicObject):
    def __init__(self,
                 id,
                 name,
                 icon,
                 mts_icon,
                 geocell_icon,
                 id_for_from,
                 restrictions,
                 restrictions2,
                 parent_id=None,
                 client=None,
                 **kwargs):
        self.id = id
        self.name = name
        self.icon = icon
        self.mts_icon = mts_icon
        self.geocell_icon = geocell_icon
        self.id_for_from = id_for_from
        self.restrictions = restrictions
        self.restrictions2 = restrictions2

        self.parent_id = parent_id

        self.client = client

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(Station, cls).de_json(data, client)
        from yandex_music import Id, Icon, Restrictions
        data['id'] = Id.de_json(data.get('id'), client)
        data['parent_id'] = Id.de_json(data.get('parent_id'), client)
        data['icon'] = Icon.de_json(data.get('icon'), client)
        data['mts_icon'] = Icon.de_json(data.get('mts_icon'), client)
        data['geocell_icon'] = Icon.de_json(data.get('geocell_icon'), client)
        data['restrictions'] = Restrictions.de_json(data.get('restrictions'), client)
        data['restrictions2'] = Restrictions.de_json(data.get('restrictions2'), client)

        return cls(client=client, **data)
