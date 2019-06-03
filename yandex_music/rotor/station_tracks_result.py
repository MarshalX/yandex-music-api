from yandex_music import YandexMusicObject


class StationTracksResult(YandexMusicObject):
    def __init__(self,
                 id,
                 sequence,
                 batch_id,
                 pumpkin,
                 client=None,
                 **kwargs):
        self.id = id
        self.sequence = sequence
        self.batch_id = batch_id
        self.pumpkin = pumpkin

        self.client = client

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(StationTracksResult, cls).de_json(data, client)
        from yandex_music import Id, Sequence
        data['id'] = Id.de_json(data.get('id'), client)
        data['sequence'] = Sequence.de_list(data.get('sequence'), client)

        return cls(client=client, **data)
