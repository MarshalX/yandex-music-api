from datetime import datetime

from yandex_music import YandexMusicObject


class TrackShort(YandexMusicObject):
    def __init__(self,
                 id,
                 timestamp,
                 album_id=None,
                 client=None,
                 **kwargs):
        self.id = id
        self.timestamp = datetime.fromisoformat(timestamp)

        self.album_id = album_id

        self._track = None

        self.client = client

    @property
    def track(self):
        if self._track:
            return self._track

        self._track = self.client.tracks(self.track_id)[0]

        return self._track

    @property
    def track_id(self):
        return f'{self.id}{":" + self.album_id if self.album_id else ""}'

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(TrackShort, cls).de_json(data, client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data, client):
        if not data:
            return []

        tracks = list()
        for track in data:
            tracks.append(cls.de_json(track, client))

        return tracks
