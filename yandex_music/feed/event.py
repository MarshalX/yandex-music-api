from yandex_music import YandexMusicObject


class Event(YandexMusicObject):
    def __init__(self,
                 id,
                 type,
                 type_for_from=None,
                 title=None,
                 tracks=None,
                 artists=None,
                 albums=None,
                 message=None,
                 device=None,
                 tracks_count=None,
                 client=None,
                 **kwargs):
        self.id = id
        self.type = type

        self.type_for_from = type_for_from
        self.title = title
        self.tracks = tracks
        self.albums = albums
        self.artists = artists
        self.message = message
        self.device = device
        self.tracks_count = tracks_count

        self.client = client

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(Event, cls).de_json(data, client)
        from yandex_music import Track, AlbumEvent, ArtistEvent
        data['tracks'] = Track.de_list(data.get('tracks'), client)
        data['albums'] = AlbumEvent.de_list(data.get('albums'), client)
        data['artists'] = ArtistEvent.de_list(data.get('artists'), client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data, client):
        if not data:
            return []

        events = list()
        for event in data:
            events.append(cls.de_json(event, client))

        return events
