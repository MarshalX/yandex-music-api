from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType, SimilarEntityItem


@model
class PlaylistSimilarEntities(YandexMusicModel):
    """Класс, представляющий похожие сущности для плейлиста.

    Attributes:
        items (:obj:`list` из :obj:`yandex_music.SimilarEntityItem`, optional): Список похожих сущностей.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    items: Optional[List['SimilarEntityItem']] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.items,)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['PlaylistSimilarEntities']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.PlaylistSimilarEntities`: Похожие сущности для плейлиста.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music import SimilarEntityItem

        cls_data['items'] = SimilarEntityItem.de_list(cls_data.get('items'), client)

        return cls(client=client, **cls_data)
