from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, Sequence


@model
class RotorSessionTracks(YandexMusicModel):
    """Класс, представляющий следующую партию треков сессии радио.

    Attributes:
        batch_id (:obj:`str`, optional): Уникальный идентификатор партии треков.
        pumpkin (:obj:`bool`, optional): TODO.
        sequence (:obj:`list` из :obj:`yandex_music.Sequence`, optional): Последовательность треков.
        terminated (:obj:`bool`, optional): Завершена ли сессия.
        unknown_session (:obj:`bool`, optional): Не найдена ли сессия с переданным идентификатором.
        offline_recommender_data (:obj:`list` из :obj:`int`, optional): Данные для офлайн-рекомендаций.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    batch_id: Optional[str] = None
    pumpkin: Optional[bool] = None
    sequence: Optional[List['Sequence']] = None
    terminated: Optional[bool] = None
    unknown_session: Optional[bool] = None
    offline_recommender_data: Optional[List[int]] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.batch_id, self.sequence)
