from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ChartInfoMenuItem, ClientType


@model
class ChartInfoMenu(YandexMusicModel):
    """Класс, представляющий меню чарта.

    Attributes:
        items (:obj:`list` из :obj:`yandex_music.ChartInfoMenuItem`): Список элементов меню.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    items: List['ChartInfoMenuItem']
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.items,)
