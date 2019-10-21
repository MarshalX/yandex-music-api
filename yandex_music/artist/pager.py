from yandex_music import YandexMusicObject

class Pager(YandexMusicObject):
    def __init__(self,
                 total,
                 page,
                 per_page,
                 client=None,
                 **kwargs):
        self.total = total
        self.page = page
        self.per_page = per_page

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(Pager, cls).de_json(data, client)

        return cls(client=client, **data)
