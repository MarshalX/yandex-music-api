from yandex_music import YandexMusicObject


class AlbumEvent(YandexMusicObject):
    def __init__(self,
                 album,
                 tracks,
                 client=None,
                 **kwargs):
        self.album = album
        self.tracks = tracks

        self.client = client

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(AlbumEvent, cls).de_json(data, client)
        from yandex_music import Album, Track
        data['album'] = Album.de_json(data.get('album'), client)
        data['tracks'] = Track.de_list(data.get('tracks'), client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data, client):
        if not data:
            return []

        album_events = list()
        for album_event in data:
            album_events.append(cls.de_json(album_event, client))

        return album_events
