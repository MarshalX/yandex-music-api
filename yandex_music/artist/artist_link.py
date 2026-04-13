from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType


@model
class ArtistLink(YandexMusicModel):
    """Класс, представляющий ссылку на страницу артиста.

    Attributes:
        title (:obj:`str`): Название ссылки.
        subtitle (:obj:`str`, optional): Подзаголовок ссылки.
        url (:obj:`str`, optional): URL ссылки.
        img_url (:obj:`str`, optional): URL изображения.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    title: str
    subtitle: Optional[str] = None
    url: Optional[str] = None
    img_url: Optional[str] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.title, self.url)
