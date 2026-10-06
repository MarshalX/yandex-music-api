from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, Track


@model
class TrackWithAds(YandexMusicModel):
    """Класс, представляющий трек с рекламой.

    Note:
        Поле `type` встречалось только с значением `track`.

    Attributes:
        type (:obj:`str`): Тип TODO.
        track (:obj:`yandex_music.Track`): Трек.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    type: str
    track: Optional['Track']
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.type, self.track)
