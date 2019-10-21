from yandex_music import YandexMusicObject

class ArtistsTracks(YandexMusicObject):
    def __init__(self,
                 tracks,
                 pager,
                 client=None,
                 **kwargs):
        self.tracks = tracks
        self.pager = pager

        self.client = client

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(ArtistsTracks, cls).de_json(data, client)
        from yandex_music import Track, Pager
        data['tracks'] = Track.de_list(data.get('tracks'), client)
        data['pager'] = Pager.de_json(data.get('pager'), client)

        return cls(client=client, **data)
