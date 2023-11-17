from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicObject
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import AdParams, Client, RotorSettings, Station


@model
class StationResult(YandexMusicObject):
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
    prerolls: Optional[list] = None
    rup_title: str = None
    rup_description: str = None
    custom_name: Optional[str] = None
    client: Optional['Client'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.station, self.settings, self.settings2, self.ad_params)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['StationResult']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.StationResult`: Радиостанция с настройками.
        """
        if not cls.is_valid_model_data(data):
            return None

        data = super(StationResult, cls).de_json(data, client)
        from yandex_music import AdParams, RotorSettings, Station

        data['station'] = Station.de_json(data.get('station'), client)
        data['settings'] = RotorSettings.de_json(data.get('settings'), client)
        data['settings2'] = RotorSettings.de_json(data.get('settings2'), client)
        data['ad_params'] = AdParams.de_json(data.get('ad_params'), client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data: list, client: 'Client') -> List['StationResult']:
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.StationResult`: Радиостанции с настройками.
        """
        if not cls.is_valid_model_data(data, array=True):
            return []

        station_results = []
        for station_result in data:
            station_results.append(cls.de_json(station_result, client))

        return station_results
