from dataclasses import field
from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, MetatagLeaf


@model
class MetatagTree(YandexMusicModel):
    """Класс, представляющий раздел дерева метатегов.

    Note:
        Известные значения поля `navigation_id`: `moods`, `activities`, `genres`, `epochs`.

    Attributes:
        title (:obj:`str`, optional): Название раздела.
        navigation_id (:obj:`str`, optional): Идентификатор раздела навигации.
        leaves (:obj:`list` из :obj:`yandex_music.MetatagLeaf`): Листы раздела с метатегами.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    title: Optional[str] = None
    navigation_id: Optional[str] = None
    leaves: List['MetatagLeaf'] = field(default_factory=list)
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.navigation_id, self.title)
