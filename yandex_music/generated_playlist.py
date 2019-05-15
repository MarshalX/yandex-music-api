from yandex_music import YandexMusicObject


class GeneratedPlaylist(YandexMusicObject):
    def __init__(self,
                 type,
                 ready,
                 notify,
                 data,
                 client=None,
                 **kwargs):
        self.type = type
        self.ready = ready
        self.notify = notify
        self.data = data

        self.client = client

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(GeneratedPlaylist, cls).de_json(data, client)
        from yandex_music import Playlist
        data['data'] = Playlist.de_json(data.get('data'), client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data, client):
        if not data:
            return []

        generated_playlists = list()
        for generated_playlist in data:
            generated_playlists.append(cls.de_json(generated_playlist, client))

        return generated_playlists
