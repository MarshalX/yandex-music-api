from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType


@model
class Deprecation(YandexMusicModel):
    """Класс, представляющий TODO.

    Attributes:
        target_album_id (:obj:`int`): Идентификатор альбома TODO.
        status (:obj:`str`): Состояние TODO.
        done (:obj:`str`): Выполнен ли TODO.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    target_album_id: Optional[int]
    status: Optional[str]
    done: Optional[bool]
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.target_album_id, self.status, self.done)
