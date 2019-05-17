from yandex_music import YandexMusicObject


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
