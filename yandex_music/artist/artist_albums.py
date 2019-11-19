from yandex_music import YandexMusicObject


class ArtistAlbums(YandexMusicObject):
    def __init__(self,
                 albums,
                 pager,
                 client=None,
                 **kwargs):
        self.albums = albums
        self.pager = pager

        self.client = client
        self._id_attrs = (self.pager, self.albums)

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(ArtistAlbums, cls).de_json(data, client)
        from yandex_music import Album, Pager
        data['albums'] = Album.de_list(data.get('albums'), client)
        data['pager'] = Pager.de_json(data.get('pager'), client)

        return cls(client=client, **data)
