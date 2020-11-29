from typing import TYPE_CHECKING, Optional, List

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client, Station, RotorSettings, AdParams


class StationResult(YandexMusicObject):
    """Класс, представляющий радиостанцию с настройками.

    Attributes:
        station (:obj:`yandex_music.Station` | :obj:`None`): Станция.
        settings (:obj:`yandex_music.RotorSettings` | :obj:`None`): Первый набор настроек.
        settings2 (:obj:`yandex_music.RotorSettings` | :obj:`None`): Второй набор настроек.
        ad_params (:obj:`yandex_music.AdParams` | :obj:`None`): Настройки рекламы.
        explanation (:obj:`str`): TODO.
        prerolls (:obj:`list` из :obj:`str`): Прероллы TODO.
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.

    Args:
        station (:obj:`yandex_music.Station` | :obj:`None`): Станция.
        settings (:obj:`yandex_music.RotorSettings` | :obj:`None`): Первый набор настроек.
        settings2 (:obj:`yandex_music.RotorSettings` | :obj:`None`): Второй набор настроек.
        ad_params (:obj:`yandex_music.AdParams` | :obj:`None`): Настройки рекламы.
        explanation (:obj:`str`, optional): TODO.
        prerolls (:obj:`list` из :obj:`str`, optional): Прероллы TODO.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 station: Optional['Station'],
                 settings: Optional['RotorSettings'],
                 settings2: Optional['RotorSettings'],
                 ad_params: Optional['AdParams'],
                 explanation: Optional[str] = None,
                 prerolls: Optional[list] = None,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        self.station = station
        self.settings = settings
        self.settings2 = settings2
        self.ad_params = ad_params
        self.explanation = explanation
        self.prerolls = prerolls

        self.client = client
        self._id_attrs = (self.station, self.settings, self.settings2, self.ad_params)

        super().handle_unknown_kwargs(self, **kwargs)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['StationResult']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.StationResult`: Радиостанция с настройками.
        """
        if not data:
            return None

        data = super(StationResult, cls).de_json(data, client)
        from yandex_music import Station, RotorSettings, AdParams
        data['station'] = Station.de_json(data.get('station'), client)
        data['settings'] = RotorSettings.de_json(data.get('settings'), client)
        data['settings2'] = RotorSettings.de_json(data.get('settings2'), client)
        data['ad_params'] = AdParams.de_json(data.get('ad_params'), client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data: dict, client: 'Client') -> List['StationResult']:
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.StationResult`: Радиостанции с настройками.
        """
        if not data:
            return []

        station_results = list()
        for station_result in data:
            station_results.append(cls.de_json(station_result, client))

        return station_results
