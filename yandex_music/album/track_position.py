from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client


@model
class TrackPosition(YandexMusicModel):
    """Класс, представляющий позицию трека.

    Note:
        Позиция трека в альбоме, который возвращается при получении самого трека.

        Volume на фронте именуется как "Диск".

    Attributes:
        volume (:obj:`int`): Номер альбома.
        index (:obj:`int`): Порядковый номер трека.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    volume: int
    index: int
    client: Optional['Client'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.volume, self.index)
