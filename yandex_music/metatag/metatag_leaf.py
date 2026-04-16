from dataclasses import field
from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType


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

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['MetatagLeaf']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.MetatagLeaf`: Лист дерева метатегов.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        cls_data['leaves'] = MetatagLeaf.de_list(cls_data.get('leaves'), client)

        return cls(client=client, **cls_data)
