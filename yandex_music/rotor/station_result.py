from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import AdParams, ClientType, JSONType, RotorSettings, Station


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
    prerolls: Optional[list] = None
    rup_title: Optional[str] = None
    rup_description: Optional[str] = None
    custom_name: Optional[str] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.station, self.settings, self.settings2, self.ad_params)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['StationResult']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.StationResult`: Радиостанция с настройками.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music import AdParams, RotorSettings, Station

        cls_data['station'] = Station.de_json(cls_data.get('station'), client)
        cls_data['settings'] = RotorSettings.de_json(cls_data.get('settings'), client)
        cls_data['settings2'] = RotorSettings.de_json(cls_data.get('settings2'), client)
        cls_data['ad_params'] = AdParams.de_json(cls_data.get('ad_params'), client)

        return cls(client=client, **cls_data)  # type: ignore
