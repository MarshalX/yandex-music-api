from yandex_music import YandexMusicObject


class Counts(YandexMusicObject):
    def __init__(self,
                 tracks,
                 direct_albums,
                 also_albums,
                 also_tracks,
                 client=None,
                 **kwargs):
        self.tracks = tracks
        self.direct_albums = direct_albums
        self.also_albums = also_albums
        self.also_tracks = also_tracks

        self.client = client

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(Counts, cls).de_json(data, client)

        return cls(client=client, **data)
