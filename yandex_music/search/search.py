from yandex_music import YandexMusicObject


class Search(YandexMusicObject):
    def __init__(self,
                 misspell_corrected,
                 nocorrect,
                 search_request_id,
                 text,
                 best,
                 albums,
                 artists,
                 playlists,
                 tracks,
                 videos,
                 client=None,
                 **kwargs):
        self.misspell_corrected = misspell_corrected
        self.nocorrect = nocorrect
        self.search_request_id = search_request_id
        self.text = text
        self.best = best
        self.albums = albums
        self.artists = artists
        self.playlists = playlists
        self.tracks = tracks
        self.videos = videos

        self.client = client
        self._id_attrs = (self.search_request_id,)

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(Search, cls).de_json(data, client)
        from yandex_music import Best, AlbumSearchResult, ArtistSearchResult, PlaylistSearchResult, \
            TrackSearchResult, VideoSearchResult
        data['best'] = Best.de_json(data.get('best'), client)
        data['albums'] = AlbumSearchResult.de_json(data.get('albums'), client)
        data['artists'] = ArtistSearchResult.de_json(data.get('artists'), client)
        data['playlists'] = PlaylistSearchResult.de_json(data.get('playlists'), client)
        data['tracks'] = TrackSearchResult.de_json(data.get('tracks'), client)
        data['videos'] = VideoSearchResult.de_json(data.get('videos'), client)

        return cls(client=client, **data)
