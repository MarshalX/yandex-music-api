from dataclasses import field
from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType
    from yandex_music.concert.concert_location import ConcertLocation


@model
class ConcertLocations(YandexMusicModel):
    """Класс, представляющий список местоположений для фильтрации концертов.

    Attributes:
        locations (:obj:`list` из :obj:`yandex_music.ConcertLocation`): Список местоположений.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    locations: List['ConcertLocation'] = field(default_factory=list)
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.locations,)
