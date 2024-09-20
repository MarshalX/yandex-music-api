from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client


@model
class Normalization(YandexMusicModel):
    """Класс, представляющий значения для нормализации трека.

    Attributes:
        gain (:obj:`str`): Значение гейна, которое нужно применить к аудиосигналу.
        peak (:obj:`int`): Пиковая точка волны аудиосигнала.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    gain: float
    peak: int
    client: Optional['Client'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.gain, self.peak)
