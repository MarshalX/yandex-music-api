from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType


@model
class ContentRestrictions(YandexMusicModel):
    """Класс, представляющий ограничения контента.

    Attributes:
        available (:obj:`bool`, optional): Доступен ли контент.
        disclaimers (:obj:`list` из :obj:`str`, optional): Список дисклеймеров.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    available: Optional[bool] = None
    disclaimers: Optional[List[str]] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.available, self.disclaimers)
