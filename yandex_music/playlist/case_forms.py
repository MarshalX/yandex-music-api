from yandex_music import YandexMusicObject


class CaseForms(YandexMusicObject):
    def __init__(self,
                 nominative,
                 genitive,
                 dative,
                 accusative,
                 instrumental,
                 prepositional,
                 client=None,
                 **kwargs):
        self.nominative = nominative
        self.genitive = genitive
        self.dative = dative
        self.accusative = accusative
        self.instrumental = instrumental
        self.prepositional = prepositional

        self.client = client

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(CaseForms, cls).de_json(data, client)

        return cls(client=client, **data)
