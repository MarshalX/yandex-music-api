from yandex_music import YandexMusicObject


class Landing(YandexMusicObject):
    def __init__(self,
                 pumpkin,
                 content_id,
                 blocks,
                 client=None,
                 **kwargs):

        self.pumpkin = pumpkin
        self.content_id = content_id
        self.blocks = blocks

        self.client = client
        self._id_attrs = (self.content_id,)

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(Landing, cls).de_json(data, client)
        from yandex_music import Block
        data['blocks'] = Block.de_list(data.get('blocks'), client)

        return cls(client=client, **data)
