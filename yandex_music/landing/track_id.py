from yandex_music import YandexMusicObject


class TrackId(YandexMusicObject):
    def __init__(self,
                 id,
                 album_id,
                 client=None,
                 **kwargs):
        self.id = id
        self.album_id = album_id

        self.client = client
        self._id_attrs = (self.id,)

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(TrackId, cls).de_json(data, client)

        return cls(client=client, **data)
