from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, StationResult


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
