from datetime import datetime

from yandex_music import YandexMusicObject


class TrackShort(YandexMusicObject):
    def __init__(self,
                 id,
                 album_id,
                 timestamp,
                 client=None,
                 **kwargs):
        self.id = id
        self.album_id = album_id
        self.timestamp = datetime.fromisoformat(timestamp)

        self.client = client

    @property
    def track_id(self):
        return f'{self.id}:{self.album_id}'

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
