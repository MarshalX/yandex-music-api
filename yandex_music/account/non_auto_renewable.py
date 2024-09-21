from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType


@model
class NonAutoRenewable(YandexMusicModel):
    """Класс, представляющий отключённое автопродление.

    Attributes:
        start (:obj:`str`): Дата начала подписки.
        end (:obj:`str`): Дата окончания подписки.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    start: str
    end: str
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.start, self.end)
