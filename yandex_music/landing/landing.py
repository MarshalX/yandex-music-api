from typing import TYPE_CHECKING, List, Optional, Union

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Block, ClientType, JSONType


@model
class Landing(YandexMusicModel):
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
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.content_id, self.blocks)

    def __getitem__(self, item: int) -> 'Block':
        return self.blocks[item]

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['Landing']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Landing`: Лендинг.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music import Block

        cls_data['blocks'] = Block.de_list(data.get('blocks'), client)

        return cls(client=client, **cls_data)  # type: ignore
