from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType, Sequence


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

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['RotorSessionTracks']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.RotorSessionTracks`: Партия треков сессии радио.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music import Sequence

        cls_data['sequence'] = Sequence.de_list(cls_data.get('sequence'), client)

        return cls(client=client, **cls_data)
