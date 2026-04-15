from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType


@model
class Wave(YandexMusicModel):
    """Класс, представляющий волну (персональную радиостанцию).

    Attributes:
        name (:obj:`str`, optional): Название волны.
        description (:obj:`str`, optional): Описание волны.
        seeds (:obj:`list` из :obj:`str`, optional): Список сидов волны (например, ``album:12345``).
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    name: Optional[str] = None
    description: Optional[str] = None
    seeds: Optional[List[str]] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.name, self.seeds)
