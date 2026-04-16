from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType


@model
class MetatagTitle(YandexMusicModel):
    """Класс, представляющий заголовок метатега.

    Attributes:
        title (:obj:`str`, optional): Короткий заголовок.
        full_title (:obj:`str`, optional): Полный заголовок.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    title: Optional[str] = None
    full_title: Optional[str] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.title, self.full_title)
