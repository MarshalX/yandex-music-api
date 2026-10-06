from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, Value


@model
class DiscreteScale(YandexMusicModel):
    """Класс, представляющий дискретное значение.

    Note:
        Известные значения поля `type`: `discrete-scale`.

    Attributes:
        type (:obj:`str`): Тип.
        name (:obj:`str`): Название.
        min (:obj:`yandex_music.Value`): Минимальное значение.
        max (:obj:`yandex_music.Value`): Максимальное значение.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    type: str
    name: str
    min: Optional['Value']
    max: Optional['Value']
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.type, self.name, self.min, self.max)
