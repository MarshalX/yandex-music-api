from yandex_music import YandexMusicObject


class Block(YandexMusicObject):
    def __init__(self,
                 id,
                 type,
                 type_for_from,
                 title,
                 entities,
                 description=None,
                 data=None,
                 client=None,
                 **kwargs):

        self.id = id
        self.type = type
        self.type_for_from = type_for_from
        self.title = title
        self.entities = entities

        self.description = description
        self.data = data

        self.client = client
        self._id_attrs = (self.id,)

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(Block, cls).de_json(data, client)
        from yandex_music import BlockEntity, PlayContextsData, PersonalPlaylistsData
        data['entities'] = BlockEntity.de_list(data.get('entities'), client)

        block_type = data.get('type')
        if block_type == 'personal-playlists':
            data['data'] = PersonalPlaylistsData.de_json(data.get('data'), client)
        elif block_type == 'play-contexts':
            data['data'] = PlayContextsData.de_json(data.get('data'), client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data, client):
        if not data:
            return []

        blocks = list()
        for block in data:
            blocks.append(cls.de_json(block, client))

        return blocks
