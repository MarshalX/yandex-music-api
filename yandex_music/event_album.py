from yandex_music import YandexMusicObject


class EventAlbum(YandexMusicObject):
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

        data = super(EventAlbum, cls).de_json(data, client)
        from yandex_music import Album, Track
        data['album'] = Album.de_json(data.get('album'), client)
        data['tracks'] = Track.de_list(data.get('tracks'), client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data, client):
        if not data:
            return []

        event_albums = list()
        for event_album in data:
            event_albums.append(cls.de_json(event_album, client))

        return event_albums
