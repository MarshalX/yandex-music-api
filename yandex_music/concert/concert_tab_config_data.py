from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType
    from yandex_music.concert.concert_tab_range import ConcertTabRange


@model
class ConcertTabConfigData(YandexMusicModel):
    """Класс, представляющий конфигурацию вкладок концертов.

    Attributes:
        top (:obj:`yandex_music.ConcertTabRange`, optional): Диапазон для блока «Топ».
        feed (:obj:`yandex_music.ConcertTabRange`, optional): Диапазон для ленты концертов.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    top: Optional['ConcertTabRange'] = None
    feed: Optional['ConcertTabRange'] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.top, self.feed)
