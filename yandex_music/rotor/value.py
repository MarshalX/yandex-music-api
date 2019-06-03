from yandex_music import YandexMusicObject


class Value(YandexMusicObject):
    def __init__(self,
                 value,
                 name,
                 client=None,
                 **kwargs):
        self.value = value
        self.name = name

        self.client = client

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(Value, cls).de_json(data, client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data, client):
        if not data:
            return []

        values = list()
        for value in data:
            values.append(cls.de_json(value, client))

        return values

