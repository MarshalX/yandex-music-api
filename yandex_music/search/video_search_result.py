from yandex_music import SearchResult


class VideoSearchResult(SearchResult):
    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(VideoSearchResult, cls).de_json(data, client)
        from yandex_music import Video
        data['results'] = Video.de_list(data.get('results'), client)

        return cls(client=client, **data)
