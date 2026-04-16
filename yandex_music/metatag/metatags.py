from dataclasses import field
from typing import TYPE_CHECKING, Iterator, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType, MetatagTree


@model
class Metatags(YandexMusicModel):
    """Класс, представляющий дерево метатегов.

    Attributes:
        trees (:obj:`list` из :obj:`yandex_music.MetatagTree`): Разделы дерева метатегов.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    trees: List['MetatagTree'] = field(default_factory=list)
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.trees,)

    def __getitem__(self, item: int) -> 'MetatagTree':
        return self.trees[item]

    def __iter__(self) -> Iterator['MetatagTree']:
        return iter(self.trees)

    def __len__(self) -> int:
        return len(self.trees)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['Metatags']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Metatags`: Дерево метатегов.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music import MetatagTree

        cls_data['trees'] = MetatagTree.de_list(cls_data.get('trees'), client)

        return cls(client=client, **cls_data)
