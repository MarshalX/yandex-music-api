from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType


@model
class Fade(YandexMusicModel):
    """Класс, представляющий параметры затухания трека.

    Attributes:
        in_start (:obj:`float`, optional): Начало нарастания звука в секундах.
        in_stop (:obj:`float`, optional): Конец нарастания звука в секундах.
        out_start (:obj:`float`, optional): Начало затухания звука в секундах.
        out_stop (:obj:`float`, optional): Конец затухания звука в секундах.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    in_start: Optional[float] = None
    in_stop: Optional[float] = None
    out_start: Optional[float] = None
    out_stop: Optional[float] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.in_start, self.in_stop, self.out_start, self.out_stop)
