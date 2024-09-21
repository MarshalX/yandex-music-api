from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType


@model
class PlaylistAbsence(YandexMusicModel):
    """Класс, представляющий причину отсутствия плейлиста.

    Attributes:
        kind (:obj:`int`): Уникальный идентификатор плейлиста.
        reason (:obj:`str`): Причина отсутствия.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    kind: int
    reason: str
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.kind, self.reason)
