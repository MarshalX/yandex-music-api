from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, SimilarEntityItem


@model
class AlbumSimilarEntities(YandexMusicModel):
    """Класс, представляющий похожие сущности для альбома.

    Attributes:
        items (:obj:`list` из :obj:`yandex_music.SimilarEntityItem`, optional): Список похожих сущностей.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    items: Optional[List['SimilarEntityItem']] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.items,)
