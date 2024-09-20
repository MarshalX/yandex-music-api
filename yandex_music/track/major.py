from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client


@model
class Major(YandexMusicModel):
    """Класс, представляющий мейджор-лейбл звукозаписи.

    Attributes:
        id (:obj:`int`): Уникальный идентификатор.
        name (:obj:`str`): Название.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    id: int
    name: str
    client: Optional['Client'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.id, self.name)
