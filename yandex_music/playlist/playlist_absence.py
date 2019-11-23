from yandex_music import YandexMusicObject


class PlaylistAbsence(YandexMusicObject):
    def __init__(self,
                 kind,
                 reason,
                 client=None,
                 **kwargs):
        self.kind = kind
        self.reason = reason

        self.client = client
        self._id_attrs = (self.kind, self.reason)

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(PlaylistAbsence, cls).de_json(data, client)

        return cls(client=client, **data)
