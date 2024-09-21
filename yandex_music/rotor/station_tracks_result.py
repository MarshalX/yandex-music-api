from typing import TYPE_CHECKING, List, Optional

from yandex_music import JSONType, YandexMusicModel
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
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    id: Optional['Id']
    sequence: List['Sequence']
    batch_id: str
    pumpkin: bool
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.id, self.sequence, self.batch_id, self.pumpkin)

    @classmethod
    def de_json(cls, data: JSONType, client: 'ClientType') -> Optional['StationTracksResult']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.StationTracksResult`: Последовательность треков станции.
        """
        if not cls.is_dict_model_data(data):
            return None

        data = cls.cleanup_data(data, client)
        from yandex_music import Id, Sequence

        data['id'] = Id.de_json(data.get('id'), client)
        data['sequence'] = Sequence.de_list(data.get('sequence'), client)

        return cls(client=client, **data)
