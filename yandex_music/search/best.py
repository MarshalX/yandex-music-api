from yandex_music import YandexMusicObject, Artist, Album, Track, Playlist, Video


de_json_result = {
    'track': Track.de_json,
    'artist': Artist.de_json,
    'album': Album.de_json,
    'playlist': Playlist.de_json,
    'video': Video.de_json,
}


class Best(YandexMusicObject):
    def __init__(self,
                 type,
                 result,
                 text=None,
                 client=None,
                 **kwargs):
        self.type = type
        self.result = result

        self.text = text

        self.client = client

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(Best, cls).de_json(data, client)
        data['result'] = de_json_result.get(data.get('type'))(data.get('result'), client)

        return cls(client=client, **data)
