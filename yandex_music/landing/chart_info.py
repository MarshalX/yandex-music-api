from typing import TYPE_CHECKING, Optional

from yandex_music import ChartInfoMenu, Playlist, YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType


@model
class ChartInfo(YandexMusicModel):
    """Класс, представляющий чарт.

    Attributes:
        id (:obj:`str`): Уникальный идентификатор блока.
        type (:obj:`str`): Тип блока.
        type_for_from (:obj:`str`): Откуда получен блок (как к нему пришли).
        title (:obj:`str`): Заголовок.
        menu (:obj:`yandex_music.ChartInfoMenu`, optional): Меню TODO.
        chart (:obj:`yandex_music.Playlist`, optional): Плейлист.
        chart_description (:obj:`str`, optional): Описание.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    id: str
    type: str
    type_for_from: str
    title: str
    menu: Optional['ChartInfoMenu']
    chart: Optional['Playlist']
    chart_description: Optional[str] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.id,)
