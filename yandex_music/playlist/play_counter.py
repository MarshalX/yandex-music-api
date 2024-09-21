from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType


@model
class PlayCounter(YandexMusicModel):
    """Класс, представляющий счётчик дней.

    Note:
        Присутствует только у плейлиста дня. Счётчик считает количество дней подряд, на протяжении которых был
        прослушан плейлист.

    Attributes:
        value (:obj:`int`): Значение (количество дней).
        description (:obj:`str`): Описание счётчика.
        updated (:obj:`bool`): Обновлён ли сегодня (в этих сутках).
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    value: int
    description: str
    updated: bool
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.value, self.description, self.updated)
