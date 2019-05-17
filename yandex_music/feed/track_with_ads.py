from yandex_music import YandexMusicObject


class TrackWithAds(YandexMusicObject):
    def __init__(self,
                 type,
                 track,
                 client=None,
                 **kwargs):
        self.type = type
        self.track = track

        self.client = client

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(TrackWithAds, cls).de_json(data, client)
        from yandex_music import Track
        data['track'] = Track.de_json(data.get('track'), client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data, client):
        if not data:
            return []

        tracks_with_ads = list()
        for track_with_ads in data:
            tracks_with_ads.append(cls.de_json(track_with_ads, client))

        return tracks_with_ads
