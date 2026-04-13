from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType


@model
class CoverDerivedColors(YandexMusicModel):
    """Класс, представляющий производные цвета обложки.

    Attributes:
        average (:obj:`str`, optional): Средний цвет.
        wave_text (:obj:`str`, optional): Цвет текста волны.
        mini_player (:obj:`str`, optional): Цвет мини-плеера.
        accent (:obj:`str`, optional): Акцентный цвет.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    average: Optional[str] = None
    wave_text: Optional[str] = None
    mini_player: Optional[str] = None
    accent: Optional[str] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.average, self.wave_text, self.mini_player, self.accent)
