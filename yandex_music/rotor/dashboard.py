from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType, StationResult


@model
class Dashboard(YandexMusicModel):
    """Класс, представляющий рекомендованные станций пользователя.

    Attributes:
        dashboard_id (:obj:`str`): Уникальный идентификатор панели.
        stations (:obj:`list` из :obj:`yandex_music.StationResult`): Станции со всеми возможными настройками и
            параметрами.
        pumpkin (:obj:`bool`): Хэллоуин.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    dashboard_id: str
    stations: List['StationResult']
    pumpkin: bool
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.dashboard_id, self.stations, self.pumpkin)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['Dashboard']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Dashboard`: Рекомендованные станций пользователя.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music import StationResult

        cls_data['stations'] = StationResult.de_list(data.get('stations'), client)

        return cls(client=client, **cls_data)  # type: ignore
