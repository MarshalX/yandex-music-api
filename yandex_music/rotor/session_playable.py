from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType


@model
class SessionPlayable(YandexMusicModel):
    """Класс, представляющий проигрываемый объект в событии сессии радио.

    Note:
        Используется в событиях `playableItem*` (:class:`yandex_music.SessionEvent`).

        Для `type` = `track` заполняется `track_id`, для `type` = `clip` заполняется `id`.

    Attributes:
        type (:obj:`str`): Тип объекта: `track` или `clip`.
        track_id (:obj:`str`, optional): Уникальный идентификатор трека.
        id (:obj:`str`, optional): Уникальный идентификатор клипа.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    type: str
    track_id: Optional[str] = None
    id: Optional[str] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.type, self.track_id, self.id)
