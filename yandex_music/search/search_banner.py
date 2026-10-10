from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType


@model
class SearchBanner(YandexMusicModel):
    """Класс, представляющий баннер в результатах поиска.

    Attributes:
        text (:obj:`str`, optional): Текст баннера.
        text_for_search (:obj:`str`, optional): Текст, по которому показывается баннер.
        url (:obj:`str`, optional): Ссылка.
        url_scheme (:obj:`str`, optional): Ссылка со схемой.
        text_color (:obj:`str`, optional): HEX-цвет текста.
        text_background_color (:obj:`str`, optional): HEX-цвет фона текста.
        image_url (:obj:`str`, optional): Ссылка на изображение.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    text: Optional[str] = None
    text_for_search: Optional[str] = None
    url: Optional[str] = None
    url_scheme: Optional[str] = None
    text_color: Optional[str] = None
    text_background_color: Optional[str] = None
    image_url: Optional[str] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.text, self.url)
