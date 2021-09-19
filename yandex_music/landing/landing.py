from typing import TYPE_CHECKING, Optional, List, Union

from yandex_music import YandexMusicObject
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client, Block


@model
class Landing(YandexMusicObject):
    """Класс, представляющий лендинг.

    Attributes:
        pumpkin (:obj:`bool`): Хэллоуин.
        content_id (:obj:`str` | :obj:`int`): Уникальный идентификатор контента.
        blocks (:obj:`list` из :obj:`yandex_music.Block`): Блоки лендинга.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    pumpkin: bool
    content_id: Union[str, int]
    blocks: List['Block']
    client: Optional['Client'] = None

    def __post_init__(self):
        self._id_attrs = (self.content_id, self.blocks)

    def __getitem__(self, item):
        return self.blocks[item]

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Landing']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Landing`: Лендинг.
        """
        if not data:
            return None

        data = super(Landing, cls).de_json(data, client)
        from yandex_music import Block

        data['blocks'] = Block.de_list(data.get('blocks'), client)

        return cls(client=client, **data)
