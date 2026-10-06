from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, SessionEvent


@model
class SessionFeedback(YandexMusicModel):
    """Класс, представляющий обратную связь сессии радио.

    Attributes:
        event (:obj:`yandex_music.SessionEvent`): Событие.
        batch_id (:obj:`str`, optional): Уникальный идентификатор партии треков, к которой относится событие.
        from_ (:obj:`str`, optional): Откуда начато воспроизведение (например, `radio-mobile-user-onyourwave`).
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    event: Optional['SessionEvent']
    batch_id: Optional[str] = None
    from_: Optional[str] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.event, self.batch_id)
