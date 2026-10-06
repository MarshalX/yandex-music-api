from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType
    from yandex_music.pin.pin import Pin


@model
class PinsList(YandexMusicModel):
    """Класс, представляющий список закреплённых элементов.

    Attributes:
        pins (:obj:`list` из :obj:`yandex_music.Pin`, optional): Список закреплённых элементов.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    pins: Optional[List['Pin']] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.pins,)
