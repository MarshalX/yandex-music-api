from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client


@model
class PassportPhone(YandexMusicModel):
    """Класс, представляющий номер телефона пользователя.

    Attributes:
        phone (:obj:`str`): Номер телефона.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    phone: str
    client: Optional['Client'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.phone,)
