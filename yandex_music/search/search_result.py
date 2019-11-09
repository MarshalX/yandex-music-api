from yandex_music import YandexMusicObject, Artist, Album, Track, Playlist, Video


de_json_result = {
    'track': Track.de_list,
    'artist': Artist.de_list,
    'album': Album.de_list,
    'playlist': Playlist.de_list,
    'video': Video.de_list,
}


class SearchResult(YandexMusicObject):
    def __init__(self,
                 total,
                 per_page,
                 order,
                 results,
                 client=None,
                 **kwargs):
        self.total = total
        self.per_page = per_page
        self.order = order
        self.results = results

        self.client = client
        self._id_attrs = (self.total, self.per_page, self.order, self.results)

    @classmethod
    def de_json(cls, data, client, type=None):
        if not data:
            return None

        data = super(SearchResult, cls).de_json(data, client)
        data['results'] = de_json_result.get(type)(data.get('results'), client)

        return cls(client=client, **data)
