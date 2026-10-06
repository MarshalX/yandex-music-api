from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, Id, Sequence


@model
class StationTracksResult(YandexMusicModel):
    """Класс, представляющий последовательность треков станции.

    Attributes:
        id (:obj:`yandex_music.Id`): Уникальный идентификатор станции.
        sequence (:obj:`list` из :obj:`yandex_music.Sequence`): Последовательность треков.
        batch_id (:obj:`str`): Уникальный идентификатор партии (последовательности).
        pumpkin (:obj:`bool`): Хэллоуин.
        radio_session_id (:obj:`str`, optional): Уникальный идентификатор сессии радио, в рамках которой выданы треки.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    id: Optional['Id']
    sequence: List['Sequence']
    batch_id: str
    pumpkin: bool
    radio_session_id: Optional[str] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.id, self.sequence, self.batch_id, self.pumpkin)
