from yandex_music import YandexMusicObject

class Lyrics(YandexMusicObject):
    def __init__(self,
                 full_lyrics,
                 text_language,
                 client=None,
                 **kwargs):
        self.full_lyrics = full_lyrics
        self.text_language = text_language

        self.client = client

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None
        
        data = super(Lyrics, cls).de_json(data, client)

        return cls(client=client, **data)


