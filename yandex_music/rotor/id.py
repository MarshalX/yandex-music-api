from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client


@model
class Id(YandexMusicModel):
    """Класс, представляющий уникальный идентификатор станции.

    Note:
        Известные типы станций: `user`, `genre`.

    Attributes:
        type (:obj:`str`): Тип станции.
        tag (:obj:`str`): Тег станции.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    type: str
    tag: str
    client: Optional['Client'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.type, self.tag)
