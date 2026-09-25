from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType


@model
class CombinedSessionQueueItem(YandexMusicModel):
    """Класс, представляющий элемент очереди комбинированной сессии радио.

    Note:
        Используется при создании комбинированной сессии и запросе следующих элементов.

        Известные значения поля `type`: `CLIP`, `TRACK`.

    Attributes:
        type (:obj:`str`): Тип элемента.
        id (:obj:`str`): Уникальный идентификатор клипа или трека.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    type: str
    id: str
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.type, self.id)
