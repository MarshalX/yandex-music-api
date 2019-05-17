from yandex_music import SearchResult


class TrackSearchResult(SearchResult):
    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(TrackSearchResult, cls).de_json(data, client)
        from yandex_music import Track
        data['results'] = Track.de_list(data.get('results'), client)

        return cls(client=client, **data)
