from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client


@model
class Deactivation(YandexMusicModel):
    """Класс, представляющий способы деактивации мобильной услуги.

    Note:
        Известные значения поля `method`: `ussd`.

    Attributes:
        method (:obj:`str`): Метод отключения.
        instructions (:obj:`str`, optional): Инструкция.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    method: str
    instructions: Optional[str] = None
    client: Optional['Client'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.method, self.instructions)
