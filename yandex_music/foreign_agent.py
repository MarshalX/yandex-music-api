from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType


@model
class ForeignAgent(YandexMusicModel):
    """Класс, представляющий информацию о статусе иноагента.

    Note:
        Известные значения поля `reason`: `policy`.

    Attributes:
        reason (:obj:`str`, optional): Причина присвоения статуса.
        title (:obj:`str`, optional): Текст предупреждения.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    reason: Optional[str] = None
    title: Optional[str] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.reason, self.title)
