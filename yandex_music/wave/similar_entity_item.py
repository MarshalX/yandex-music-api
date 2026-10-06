from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType
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
