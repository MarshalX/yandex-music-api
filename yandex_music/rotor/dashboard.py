from typing import TYPE_CHECKING, Optional, List

from yandex_music import YandexMusicObject
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client, StationResult


@model
class Dashboard(YandexMusicObject):
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
    client: Optional['Client'] = None

    def __post_init__(self):
        self._id_attrs = (self.dashboard_id, self.stations, self.pumpkin)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Dashboard']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Dashboard`: Рекомендованные станций пользователя.
        """
        if not data:
            return None

        data = super(Dashboard, cls).de_json(data, client)
        from yandex_music import StationResult

        data['stations'] = StationResult.de_list(data.get('stations'), client)

        return cls(client=client, **data)
