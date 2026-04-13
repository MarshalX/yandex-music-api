from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType


@model
class ConcertCashback(YandexMusicModel):
    """Класс, представляющий информацию о кешбэке за покупку билета.

    Attributes:
        title (:obj:`str`, optional): Текст кешбэка, например "Кешбэк до 20%".
        value_percent (:obj:`int`, optional): Процент кешбэка.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    title: Optional[str] = None
    value_percent: Optional[int] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.title, self.value_percent)
