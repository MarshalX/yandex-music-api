from dataclasses import field
from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType


@model
class MetatagLeaf(YandexMusicModel):
    """Класс, представляющий лист дерева метатегов.

    Значение поля :attr:`tag` используется как идентификатор метатега в запросах
    к ручкам :attr:`yandex_music.Client.metatag` и родственных методов.

    Attributes:
        tag (:obj:`str`, optional): Идентификатор метатега.
        title (:obj:`str`, optional): Название метатега для отображения.
        leaves (:obj:`list` из :obj:`yandex_music.MetatagLeaf`, optional): Вложенные листы метатега.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    tag: Optional[str] = None
    title: Optional[str] = None
    leaves: List['MetatagLeaf'] = field(default_factory=list)
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.tag,)
