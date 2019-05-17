from yandex_music import YandexMusicObject


class TracksLikes(YandexMusicObject):
    def __init__(self,
                 uid,
                 revision,
                 tracks,
                 client=None,
                 **kwargs):
        self.uid = uid
        self.revision = revision
        self.tracks = tracks

        self.client = client

    @property
    def tracks_ids(self):
        return [track.track_id for track in self.tracks]

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(TracksLikes, cls).de_json(data, client)
        from yandex_music import TrackShort
        data['tracks'] = TrackShort.de_list(data.get('tracks'), client)

        return cls(client=client, **data)
