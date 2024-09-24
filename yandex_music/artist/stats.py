from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType


@model
class Stats(YandexMusicModel):
    """Класс, представляющий статистику слушателей артиста.

    Attributes:
        last_month_listeners (:obj:`int`): Количество слушателей за последний месяц.
        last_month_listeners_delta (:obj:`int`): Изменение количества слушателей за последний месяц.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    last_month_listeners: int
    last_month_listeners_delta: int
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.last_month_listeners, self.last_month_listeners_delta)
