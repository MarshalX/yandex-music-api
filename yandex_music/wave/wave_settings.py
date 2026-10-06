from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, Restrictions, WaveDefaultStation, WaveSettingsBlock


@model
class WaveSettings(YandexMusicModel):
    """Класс, представляющий настройки волны.

    Note:
        Значения из `setting_restrictions` можно передавать как сиды сессии радио
        (поле :attr:`yandex_music.Value.serialized_seed`, например, `settingDiversity:favorite`).

    Attributes:
        default_station (:obj:`yandex_music.WaveDefaultStation`, optional): Станция волны по умолчанию.
        blocks (:obj:`list` из :obj:`yandex_music.WaveSettingsBlock`, optional): Блоки настроек.
        setting_restrictions (:obj:`yandex_music.Restrictions`, optional): Доступные значения настроек волны.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    default_station: Optional['WaveDefaultStation'] = None
    blocks: Optional[List['WaveSettingsBlock']] = None
    setting_restrictions: Optional['Restrictions'] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.default_station, self.blocks, self.setting_restrictions)
