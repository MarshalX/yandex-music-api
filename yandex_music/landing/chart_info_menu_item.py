from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType


@model
class ChartInfoMenuItem(YandexMusicModel):
    """Класс, представляющий элемент меню чарта.

    Attributes:
        title (:obj:`str`): Заголовок.
        url (:obj:`str`): Постфикс для запроса чарта.
        selected (:obj:`bool`, optional): Текущий ли элемент.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    title: str
    url: str
    selected: Optional[bool] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.url, self.selected)
