from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, RotorSeed, Sequence, Wave


@model
class RotorSession(YandexMusicModel):
    """Класс, представляющий сессию радио.

    Note:
        Идентификатор сессии `radio_session_id` используется для получения следующих треков и отправки обратной связи.

    Attributes:
        radio_session_id (:obj:`str`, optional): Уникальный идентификатор сессии радио.
        batch_id (:obj:`str`, optional): Уникальный идентификатор партии треков.
        pumpkin (:obj:`bool`, optional): TODO.
        sequence (:obj:`list` из :obj:`yandex_music.Sequence`, optional): Последовательность треков.
        accepted_seeds (:obj:`list` из :obj:`yandex_music.RotorSeed`, optional): Принятые сиды.
        description_seed (:obj:`yandex_music.RotorSeed`, optional): Сид, описывающий сессию.
        terminated (:obj:`bool`, optional): Завершена ли сессия.
        wave (:obj:`yandex_music.Wave`, optional): Волна сессии. Возвращается при `include_wave_model`.
        offline_recommender_data (:obj:`list` из :obj:`int`, optional): Данные для офлайн-рекомендаций.
        interactive (:obj:`bool`, optional): Является ли сессия интерактивной.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    radio_session_id: Optional[str] = None
    batch_id: Optional[str] = None
    pumpkin: Optional[bool] = None
    sequence: Optional[List['Sequence']] = None
    accepted_seeds: Optional[List['RotorSeed']] = None
    description_seed: Optional['RotorSeed'] = None
    terminated: Optional[bool] = None
    wave: Optional['Wave'] = None
    offline_recommender_data: Optional[List[int]] = None
    interactive: Optional[bool] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.radio_session_id, self.batch_id)
