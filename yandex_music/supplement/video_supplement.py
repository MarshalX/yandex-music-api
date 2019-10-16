from yandex_music import YandexMusicObject

class VideoSupplement(YandexMusicObject):
    def __init__(self,
                 cover,
                 title,
                 embed_url,
                 client=None,
                 **kwargs):
        self.cover = cover
        self.title = title
        self.embed_url = embed_url

        self.client = client

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(VideoSupplement, cls).de_json(data, client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data, client):
        if not data:
            return []
        
        videos = list()
        for video in data:
            videos.append(cls.de_json(video, client))

        return videos