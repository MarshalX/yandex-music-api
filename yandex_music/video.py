from yandex_music import YandexMusicObject


class Video(YandexMusicObject):
    def __init__(self,
                 title,
                 cover=None,
                 embed_url=None,
                 provider=None,
                 provider_video_id=None,
                 youtube_url=None,
                 thumbnail_url=None,
                 duration=None,
                 text=None,
                 html_auto_play_video_player=None,
                 regions=None,
                 client=None,
                 **kwargs):
        self.title = title

        # Видео из brief info
        self.cover = cover
        self.embed_url = embed_url
        self.provider = provider
        self.provider_video_id = provider_video_id

        # Видео из результатов поиска
        self.youtube_url = youtube_url
        self.thumbnail_url = thumbnail_url
        self.duration = duration
        self.text = text
        self.html_auto_play_video_player = html_auto_play_video_player
        self.regions = regions

        self.client = client
        self._id_attrs = (self.provider_video_id, self.youtube_url, self.title)

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(Video, cls).de_json(data, client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data, client):
        if not data:
            return []

        videos = list()
        for video in data:
            videos.append(cls.de_json(video, client))

        return videos
