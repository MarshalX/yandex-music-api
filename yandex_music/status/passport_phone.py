from yandex_music import YandexMusicObject


class PassportPhone(YandexMusicObject):
    def __init__(self,
                 phone,
                 client=None,
                 **kwargs):
        self.phone = phone

        self.client = client
        self._id_attrs = (self.phone,)

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(PassportPhone, cls).de_json(data, client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data, client):
        if not data:
            return []

        phones = list()
        for phone in data:
            phones.append(cls.de_json(phone, client))

        return phones
