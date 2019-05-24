from yandex_music import YandexMusicObject


class PlayContextsData(YandexMusicObject):
    def __init__(self,
                 other_tracks,
                 client=None,
                 **kwargs):
        self.other_tracks = other_tracks

        self.client = client

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(PlayContextsData, cls).de_json(data, client)
        from yandex_music import TrackShortOld
        data['other_tracks'] = TrackShortOld.de_list(data.get('other_tracks'), client)

        return cls(client=client, **data)
