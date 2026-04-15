from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType
    from yandex_music.wave.similar_entity_data import SimilarEntityData


@model
class SimilarEntityItem(YandexMusicModel):
    """Класс, представляющий элемент списка похожих сущностей.

    Note:
        Известные значения поля `type`: ``wave_agent_item``.

    Attributes:
        type (:obj:`str`, optional): Тип элемента.
        data (:obj:`yandex_music.SimilarEntityData`, optional): Данные элемента.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    type: Optional[str] = None
    data: Optional['SimilarEntityData'] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.type, self.data)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['SimilarEntityItem']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.SimilarEntityItem`: Элемент списка похожих сущностей.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music.wave.similar_entity_data import SimilarEntityData

        cls_data['data'] = SimilarEntityData.de_json(cls_data.get('data'), client)

        return cls(client=client, **cls_data)
