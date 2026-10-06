from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType
    from yandex_music.concert.concert_tab_config_data import ConcertTabConfigData


@model
class ConcertTabConfig(YandexMusicModel):
    """Класс, представляющий конфигурацию вкладок ленты концертов.

    Attributes:
        config (:obj:`yandex_music.ConcertTabConfigData`, optional): Конфигурация вкладок концертов.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    config: Optional['ConcertTabConfigData'] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.config,)
