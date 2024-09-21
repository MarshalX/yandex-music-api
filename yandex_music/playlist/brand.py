from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType


@model
class Brand(YandexMusicModel):
    """Класс, представляющий бренд плейлиста.

    Note:
        Отслеживание просмотров на сторонник сервисах бренда, рекомендация следующего контента.

    Attributes:
        image (:obj:`str`): Ссылка на изображение.
        background (:obj:`str`): Цвет заднего фона.
        reference (:obj:`str`): URI ссылка на содержимое.
        pixels (:obj:`list` из :obj:`str`): Ссылки на gif изображения для отслеживания просмотров (web beacon).
        theme (:obj:`str`): Тема оформления.
        playlist_theme (:obj:`str`): Тема плейлиста TODO.
        button (:obj:`str`): Текст кнопки.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    image: str
    background: str
    reference: str
    pixels: List[str]
    theme: str
    playlist_theme: str
    button: str
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.image, self.reference, self.pixels)
