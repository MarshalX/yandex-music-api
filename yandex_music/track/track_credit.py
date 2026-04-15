from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType


@model
class TrackCredit(YandexMusicModel):
    """Класс, представляющий информацию об участнике создания трека.

    Attributes:
        title (:obj:`str`, optional): Роль участника (например, «Автор музыки», «Лейбл»).
        value (:obj:`str`, optional): Имя или название участника.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    title: Optional[str] = None
    value: Optional[str] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.title, self.value)
