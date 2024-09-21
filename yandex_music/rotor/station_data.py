from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType


@model
class StationData(YandexMusicModel):
    """Класс, представляющий информацию о личной станции.

    Attributes:
        name (:obj:`str`): Название станции.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    name: str
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.name,)
