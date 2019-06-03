from yandex_music import YandexMusicObject


class DiscreteScale(YandexMusicObject):
    def __init__(self,
                 type,
                 name,
                 min,
                 max,
                 client=None,
                 **kwargs):
        self.type = type
        self.name = name
        self.min = min
        self.max = max

        self.client = client

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(DiscreteScale, cls).de_json(data, client)
        from yandex_music import Value
        data['min'] = Value.de_json(data.get('min'), client)
        data['max'] = Value.de_json(data.get('max'), client)

        return cls(client=client, **data)
