from yandex_music import SearchResult


class ArtistSearchResult(SearchResult):
    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(ArtistSearchResult, cls).de_json(data, client)
        from yandex_music import Artist
        data['results'] = Artist.de_list(data.get('results'), client)

        return cls(client=client, **data)
