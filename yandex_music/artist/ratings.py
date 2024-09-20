from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client


@model
class Ratings(YandexMusicModel):
    """Класс, представляющий рейтинг исполнителя.

    Attributes:
        month (:obj:`int`): Значение ежемесячного рейтинга.
        week (:obj:`int`, optional): Значение еженедельного рейтинга.
        day (:obj:`int`, optional): Значение дневного рейтинга.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    month: int
    week: Optional[int] = None
    day: Optional[int] = None
    client: Optional['Client'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.week, self.month)
