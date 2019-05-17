from yandex_music import SearchResult


class PlaylistSearchResult(SearchResult):
    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(PlaylistSearchResult, cls).de_json(data, client)
        from yandex_music import Playlist
        data['results'] = Playlist.de_list(data.get('results'), client)

        return cls(client=client, **data)
