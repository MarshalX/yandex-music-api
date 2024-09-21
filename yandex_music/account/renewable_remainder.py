from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType


@model
class RenewableRemainder(YandexMusicModel):
    """Класс, представляющий напоминания о продлении подписки.

    Note:
        Присутствует только тогда, когда автопродление отключено.

    Attributes:
        days (:obj:`int`): Количество дней (до окончания подписки, по всей видимости).
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    days: int
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.days,)
