from yandex_music import SearchResult


class AlbumSearchResult(SearchResult):
    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(AlbumSearchResult, cls).de_json(data, client)
        from yandex_music import Album
        data['results'] = Album.de_list(data.get('results'), client)

        return cls(client=client, **data)
