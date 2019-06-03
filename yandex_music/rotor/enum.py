from yandex_music import YandexMusicObject


class Enum(YandexMusicObject):
    def __init__(self,
                 type,
                 name,
                 possible_values,
                 client=None,
                 **kwargs):
        self.type = type
        self.name = name
        self.possible_values = possible_values

        self.client = client

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(Enum, cls).de_json(data, client)
        from yandex_music import Value
        data['possible_values'] = Value.de_list(data.get('possible_values'), client)

        return cls(client=client, **data)
