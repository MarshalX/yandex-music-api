from yandex_music import YandexMusicObject


class Label(YandexMusicObject):
    def __init__(self,
                 id,
                 name,
                 client=None,
                 **kwargs):
        self.id = id
        self.name = name

        self.client = client
        self._id_attrs = (self.id,)

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(Label, cls).de_json(data, client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data, client):
        if not data:
            return []

        labels = list()
        for label in data:
            labels.append(cls.de_json(label, client))

        return labels
