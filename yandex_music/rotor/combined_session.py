from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, CombinedSessionItem


@model
class CombinedSession(YandexMusicModel):
    """Класс, представляющий комбинированную сессию радио (треки и клипы).

    Note:
        Поле `session_id` приходит только при создании сессии.

    Attributes:
        session_id (:obj:`str`, optional): Уникальный идентификатор сессии.
        batch_id (:obj:`str`, optional): Уникальный идентификатор партии элементов.
        pumpkin (:obj:`bool`, optional): TODO.
        list (:obj:`list` из :obj:`yandex_music.CombinedSessionItem`, optional): Элементы сессии.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    session_id: Optional[str] = None
    batch_id: Optional[str] = None
    pumpkin: Optional[bool] = None
    list: Optional[List['CombinedSessionItem']] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.session_id, self.batch_id)
