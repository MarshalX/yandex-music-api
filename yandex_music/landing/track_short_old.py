from yandex_music import YandexMusicObject


class TrackShortOld(YandexMusicObject):
    def __init__(self,
                 track_id,
                 timestamp,
                 client=None,
                 **kwargs):
        self.track_id = track_id
        self.timestamp = timestamp

        self.client = client
        self._id_attrs = (self.track_id,)

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(TrackShortOld, cls).de_json(data, client)
        from yandex_music import TrackId
        data['track_id'] = TrackId.de_json(data.get('track_id'), client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data, client):
        if not data:
            return []

        tracks = list()
        for track in data:
            tracks.append(cls.de_json(track, client))

        return tracks
