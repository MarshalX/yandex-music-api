from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client


@model
class LyricsMajor(YandexMusicModel):
    """Класс, представляющий сервис-источник текстов к трекам.

    Args:
        id (:obj:`int`): Уникальный идентификатор сервиса.
        name (:obj:`str`): Имя сервиса.
        pretty_name (:obj:`str`): Человекочитаемое имя сервиса.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    id: int
    name: str
    pretty_name: str
    client: Optional['Client'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.id,)
