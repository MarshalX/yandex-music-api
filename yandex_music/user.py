from yandex_music import YandexMusicObject


class User(YandexMusicObject):
    def __init__(self,
                 uid,
                 login,
                 name,
                 sex,
                 verified,
                 client=None,
                 **kwargs):
        self.uid = uid
        self.login = login
        self.name = name
        self.sex = sex
        self.verified = verified

        self.client = client
        self._id_attrs = (self.uid,)

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(User, cls).de_json(data, client)

        return cls(client=client, **data)
