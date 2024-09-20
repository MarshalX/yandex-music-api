from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client


@model
class Link(YandexMusicModel):
    """Класс, представляющий ссылку на официальную страницу исполнителя.

    Note:
        Известные типы страниц: `official` - официальный сайт и `social` - социальная сеть.

    Attributes:
        title (:obj:`str`): Название страницы.
        href (:obj:`str`): URL страницы.
        type (:obj:`str`): Тип страницы.
        social_network (:obj:`str`, optional): Название социальной сети.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    title: str
    href: str
    type: str
    social_network: Optional[str] = None
    client: Optional['Client'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.title, self.href, self.type)
