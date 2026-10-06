from typing import TYPE_CHECKING, List, Optional, Union

from typing_extensions import override

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Block, ClientType


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

    @override
    def __getitem__(self, item: int) -> 'Block':
        return self.blocks[item]
