from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType, RotorSeed, Sequence, Wave


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

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['RotorSession']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.RotorSession`: Сессия радио.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music import RotorSeed, Sequence, Wave

        cls_data['sequence'] = Sequence.de_list(cls_data.get('sequence'), client)
        cls_data['accepted_seeds'] = RotorSeed.de_list(cls_data.get('accepted_seeds'), client)
        cls_data['description_seed'] = RotorSeed.de_json(cls_data.get('description_seed'), client)
        cls_data['wave'] = Wave.de_json(cls_data.get('wave'), client)

        return cls(client=client, **cls_data)
