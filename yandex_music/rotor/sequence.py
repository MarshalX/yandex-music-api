from yandex_music import YandexMusicObject


class Sequence(YandexMusicObject):
    def __init__(self,
                 type,
                 track,
                 liked,
                 client=None,
                 **kwargs):
        self.type = type
        self.track = track
        self.liked = liked

        self.client = client

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(Sequence, cls).de_json(data, client)
        from yandex_music import Track
        data['track'] = Track.de_json(data.get('track'), client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data, client):
        if not data:
            return []

        sequences = list()
        for sequence in data:
            sequences.append(cls.de_json(sequence, client))

        return sequences
