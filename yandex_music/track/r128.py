from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType


@model
class R128(YandexMusicModel):
    """Класс, описывающий параметры нормализации громкости трека в соответствии с рекомендацией EBU R 128.

    Attributes:
        i (:obj:`float`): Интегрированная громкость. Совокупная громкость от начала до конца.
        tp (:obj:`float`): True Peak. Реконструкция пикового уровня сигнала между выборками
            (пикового уровня, генерируемого между двумя выборками ), рассчитанного с помощью
            передискретизации.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    i: float
    tp: float
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.i, self.tp)
