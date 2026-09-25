from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType


@model
class WaveDefaultStation(YandexMusicModel):
    """Класс, представляющий станцию волны по умолчанию.

    Attributes:
        station_id (:obj:`str`, optional): Идентификатор станции (например, ``user:12345``).
        title (:obj:`str`, optional): Название станции.
        rup_title (:obj:`str`, optional): Заголовок станции.
        rup_description (:obj:`str`, optional): Описание станции.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    station_id: Optional[str] = None
    title: Optional[str] = None
    rup_title: Optional[str] = None
    rup_description: Optional[str] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.station_id, self.title)
