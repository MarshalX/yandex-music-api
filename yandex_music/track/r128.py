from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicObject
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client


@model
class R128(YandexMusicObject):
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
    client: Optional['Client'] = None

    def __post_init__(self):
        self._id_attrs = (self.i, self.tp)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['R128']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.R128`: Параметры нормализации громкости трека в соответствии с рекомендацией EBU R 128.
        """
        if not data:
            return None

        data = super(R128, cls).de_json(data, client)

        return cls(client=client, **data)
