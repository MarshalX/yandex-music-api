from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType
    from yandex_music.pin.pin_data import PinData


@model
class Pin(YandexMusicModel):
    """Класс, представляющий закреплённый элемент.

    Note:
        Известные значения поля `type`: `artist_item`, `album_item`, `playlist_item`, `wave_item`.

    Attributes:
        type (:obj:`str`): Тип закреплённого элемента.
        data (:obj:`yandex_music.PinData`, optional): Данные закреплённого элемента.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    type: str
    data: Optional['PinData'] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.type, self.data)
