from dataclasses import field
from typing import TYPE_CHECKING, Iterator, List, Optional

from typing_extensions import override

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, MetatagTree


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

    @override
    def __getitem__(self, item: int) -> 'MetatagTree':
        return self.trees[item]

    def __iter__(self) -> Iterator['MetatagTree']:
        return iter(self.trees)

    def __len__(self) -> int:
        return len(self.trees)
