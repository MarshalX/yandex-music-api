from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, SessionFeedback


@model
class SessionFeedbacks(YandexMusicModel):
    """Класс, представляющий набор обратной связи одной сессии радио.

    Note:
        Используется для отправки обратной связи сразу по нескольким сессиям.

    Attributes:
        session_id (:obj:`str`): Уникальный идентификатор сессии радио.
        feedbacks (:obj:`list` из :obj:`yandex_music.SessionFeedback`): Обратная связь.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    session_id: str
    feedbacks: List['SessionFeedback']
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.session_id, self.feedbacks)
