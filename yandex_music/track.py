from yandex_music import YandexMusicObject


class Track(YandexMusicObject):
    def __init__(self,
                 id,
                 real_id,
                 title,
                 available,
                 available_for_premium_users,
                 artists,
                 albums,
                 og_image,
                 lyrics_available,
                 type,
                 cover_uri=None,
                 major=None,
                 duration_ms=None,
                 storage_dir=None,
                 file_size=None,
                 normalization=None,
                 error=None,
                 client=None,
                 **kwargs):
        self.id = id
        self.real_id = real_id
        self.title = title
        self.available = available
        self.available_for_premium_users = available_for_premium_users
        self.artists = artists
        self.albums = albums
        self.og_image = og_image
        self.lyrics_available = lyrics_available
        self.type = type

        self.cover_uri = cover_uri
        self.major = major
        self.duration_ms = duration_ms
        self.storage_dir = storage_dir
        self.file_size = file_size
        self.normalization = normalization
        self.error = error

        self.client = client
        self._id_attrs = (self.id,)

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(Track, cls).de_json(data, client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data, client):
        if not data:
            return []

        tracks = list()
        for track in data:
            tracks.append(cls.de_json(track, client))

        return tracks
