from yandex_music import YandexMusicObject


class Suggestions(YandexMusicObject):
    def __init__(self,
                 best,
                 suggestions,
                 client=None,
                 **kwargs):
        self.best = best
        self._suggestions = suggestions

        self.client = client

    def __getitem__(self, item):
        return self._suggestions[item]

    def __iter__(self):
        return iter(self._suggestions)

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(Suggestions, cls).de_json(data, client)
        from yandex_music import Best
        data['best'] = Best.de_json(data.get('best'), client)

        return cls(client=client, **data)

