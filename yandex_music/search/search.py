from yandex_music import YandexMusicObject


class Search(YandexMusicObject):
    def __init__(self,
                 search_request_id,
                 text,
                 best,
                 albums,
                 artists,
                 playlists,
                 tracks,
                 videos,
                 misspell_corrected=None,
                 nocorrect=None,
                 client=None,
                 **kwargs):
        self.search_request_id = search_request_id
        self.text = text
        self.best = best
        self.albums = albums
        self.artists = artists
        self.playlists = playlists
        self.tracks = tracks
        self.videos = videos

        self.misspell_corrected = misspell_corrected
        self.nocorrect = nocorrect

        self.client = client
        self._id_attrs = (self.search_request_id, self.text, self.best, self.albums,
                          self.artists, self.playlists, self.tracks, self.videos)

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(Search, cls).de_json(data, client)
        from yandex_music import SearchResult, Best
        data['best'] = Best.de_json(data.get('best'), client)
        data['albums'] = SearchResult.de_json(data.get('albums'), client, 'album')
        data['artists'] = SearchResult.de_json(data.get('artists'), client, 'artist')
        data['playlists'] = SearchResult.de_json(data.get('playlists'), client, 'playlist')
        data['tracks'] = SearchResult.de_json(data.get('tracks'), client, 'track')
        data['videos'] = SearchResult.de_json(data.get('videos'), client, 'video')

        return cls(client=client, **data)
