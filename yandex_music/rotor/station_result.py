from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import AdParams, ClientType, RotorSettings, Station


@model
class StationResult(YandexMusicModel):
    """Класс, представляющий радиостанцию с настройками.

    Note:
        Известные значения `custom_name`: `Танцую`, `R'n'B`, `Отдыхаю`, `Просыпаюсь`,
        `Тренируюсь`, `В дороге`, `Работаю`, `Засыпаю`.

    Attributes:
        station (:obj:`yandex_music.Station` | :obj:`None`): Станция.
        settings (:obj:`yandex_music.RotorSettings` | :obj:`None`): Первый набор настроек.
        settings2 (:obj:`yandex_music.RotorSettings` | :obj:`None`): Второй набор настроек.
        ad_params (:obj:`yandex_music.AdParams` | :obj:`None`): Настройки рекламы.
        explanation (:obj:`str`, optional): TODO.
        prerolls (:obj:`list` из :obj:`str`, optional): Прероллы TODO.
        rup_title (:obj:`str`): Название станции / Моя волна TODO.
        rup_description (:obj:`str`): Описание станции.
        custom_name (:obj:`str`, optional): Название станции TODO.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    station: Optional['Station']
    settings: Optional['RotorSettings']
    settings2: Optional['RotorSettings']
    ad_params: Optional['AdParams']
    explanation: Optional[str] = None
    prerolls: Optional[List[str]] = None
    rup_title: Optional[str] = None
    rup_description: Optional[str] = None
    custom_name: Optional[str] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.station, self.settings, self.settings2, self.ad_params)
