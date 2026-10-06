from dataclasses import field
from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, Cover
    from yandex_music.concert.concert import Concert
    from yandex_music.concert.concert_description import ConcertDescription
    from yandex_music.concert.concert_min_price import ConcertMinPrice


@model
class ConcertInfo(YandexMusicModel):
    """Класс, представляющий информацию о концерте.

    Attributes:
        concert (:obj:`yandex_music.Concert`, optional): Концерт.
        min_price (:obj:`yandex_music.ConcertMinPrice`, optional): Минимальная цена билета.
        covers (:obj:`list` из :obj:`yandex_music.Cover`): Дополнительные обложки концерта.
        description (:obj:`yandex_music.ConcertDescription`, optional): Описание концерта.
        lead_artist_id (:obj:`int`, optional): Уникальный идентификатор ведущего артиста.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    concert: Optional['Concert'] = None
    min_price: Optional['ConcertMinPrice'] = None
    covers: List['Cover'] = field(default_factory=list)
    description: Optional['ConcertDescription'] = None
    lead_artist_id: Optional[int] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.concert,)
