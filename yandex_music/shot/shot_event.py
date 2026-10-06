from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, Shot


@model
class ShotEvent(YandexMusicModel):
    """Класс, представляющий событие-шот перед началом следующего трека.

    Attributes:
        event_id (:obj:`str`): Уникальный идентификатор события.
        shots (:obj:`list` из :obj:`yandex_music.Shot`): Шоты от Алисы.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    event_id: str
    shots: List['Shot']
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.event_id, self.shots)
