from typing import TYPE_CHECKING, Optional, List, Union

if TYPE_CHECKING:
    from yandex_music import Client, Block

from yandex_music import YandexMusicObject


class Landing(YandexMusicObject):
    def __init__(self,
                 pumpkin: bool,
                 content_id: Union[str, int],
                 blocks: List['Block'],
                 client: Optional['Client'] = None,
                 **kwargs) -> None:

        self.pumpkin = pumpkin
        self.content_id = content_id
        self.blocks = blocks

        self.client = client
        self._id_attrs = (self.content_id, self.blocks)

    def __getitem__(self, item):
        return self.blocks[item]

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Landing']:
        if not data:
            return None

        data = super(Landing, cls).de_json(data, client)
        from yandex_music import Block
        data['blocks'] = Block.de_list(data.get('blocks'), client)

        return cls(client=client, **data)
