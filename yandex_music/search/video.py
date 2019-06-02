from yandex_music import YandexMusicObject


class Video(YandexMusicObject):
    def __init__(self,
                 youtube_url,
                 thumbnail_url,
                 title,
                 duration,
                 text,
                 html_auto_play_video_player,
                 regions,
                 client=None,
                 **kwargs):
        self.youtube_url = youtube_url
        self.thumbnail_url = thumbnail_url
        self.title = title
        self.duration = duration
        self.text = text
        self.html_auto_play_video_player = html_auto_play_video_player
        self.regions = regions

        self.client = client

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
