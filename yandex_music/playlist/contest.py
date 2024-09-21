from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType


@model
class Contest(YandexMusicModel):
    """Класс, представляющий контест TODO.

    Note:
        Известные значения поля `status`: `editing`, `withdrew-moderator`.

    Attributes:
        contest_id (:obj:`str`): Уникальный идентификатор.
        status (:obj:`str`): Статус.
        can_edit (:obj:`bool`): Разрешено ли редактирование.
        sent (:obj:`str`, optional): Дата отправки.
        withdrawn (:obj:`str`, optional): Дата вывода (окончания).
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    contest_id: str
    status: str
    can_edit: bool
    sent: Optional[str] = None
    withdrawn: Optional[str] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.contest_id, self.status)
