from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client


@model
class Value(YandexMusicModel):
    """Класс, представляющий значение(переменную).

    Attributes:
        value (:obj:`str`): Значение.
        name (:obj:`str`): Название.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    value: str
    name: str
    client: Optional['Client'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.value, self.name)
