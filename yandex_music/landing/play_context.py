from yandex_music import YandexMusicObject


class PlayContext(YandexMusicObject):
    def __init__(self,
                 client_,
                 context,
                 context_item,
                 tracks,
                 client=None,
                 **kwargs):

        self.client_ = client_
        self.context = context
        self.context_item = context_item
        self.tracks = tracks
        self.client = client

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(PlayContext, cls).de_json(data, client)
        from yandex_music import TrackShortOld
        data['tracks'] = TrackShortOld.de_list(data.get('tracks'), client)

        return cls(client=client, **data)
