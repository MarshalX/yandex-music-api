from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, Station


@model
class WaveSettingsBlock(YandexMusicModel):
    """Класс, представляющий блок настроек волны.

    Note:
        Известные значения поля `type`: `contexts`.

    Attributes:
        type (:obj:`str`, optional): Тип блока.
        items (:obj:`list` из :obj:`yandex_music.Station`, optional): Станции-контексты блока (например, занятия).
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    type: Optional[str] = None
    items: Optional[List['Station']] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.type, self.items)
