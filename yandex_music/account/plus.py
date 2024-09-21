from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType


@model
class Plus(YandexMusicModel):
    """Класс, представляющий `Plus` подписку.

    Attributes:
        has_plus (:obj:`bool`): Наличие.
        is_tutorial_completed (:obj:`bool`): Закончено ли руководство.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    has_plus: bool
    is_tutorial_completed: bool
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.has_plus, self.is_tutorial_completed)
