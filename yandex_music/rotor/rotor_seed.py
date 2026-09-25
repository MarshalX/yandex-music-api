from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType


@model
class RotorSeed(YandexMusicModel):
    """Класс, представляющий сид радио.

    Note:
        Сид в строковом виде записывается как `type:tag`, например, `user:onyourwave`, `genre:rock`,
        `track:12345`, `settingDiversity:discover`.

    Attributes:
        type (:obj:`str`, optional): Тип сида.
        tag (:obj:`str`, optional): Тег сида.
        value (:obj:`str`, optional): Значение сида.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    type: Optional[str] = None
    tag: Optional[str] = None
    value: Optional[str] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.type, self.tag, self.value)
