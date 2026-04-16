from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType


@model
class AlbumActionButton(YandexMusicModel):
    """Класс, представляющий кнопку-действие альбома.

    Attributes:
        text (:obj:`str`, optional): Текст кнопки.
        url (:obj:`str`, optional): URL-ссылка.
        color (:obj:`str`, optional): HEX-цвет кнопки.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    text: Optional[str] = None
    url: Optional[str] = None
    color: Optional[str] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.text, self.url, self.color)
