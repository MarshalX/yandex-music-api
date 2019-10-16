from yandex_music import YandexMusicObject

class Supplement(YandexMusicObject):
    def __init__(self,
                 lyrics,
                 videos,
                 client=None,
                 **kwargs):
        self.lyrics = lyrics
        self.videos = videos

        self.client = client

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(Supplement, cls).de_json(data, client)
        from yandex_music import Lyrics, VideoSupplement
        data['lyrics'] = Lyrics.de_json(data['lyrics'], client)
        data['videos'] = VideoSupplement.de_list(data['videos'], client)

        return cls(client=client, **data)
