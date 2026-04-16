from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType


@model
class ConcertTabRange(YandexMusicModel):
    """Класс, представляющий диапазон пагинации вкладки концертов.

    Attributes:
        offset (:obj:`int`, optional): Смещение от начала выборки.
        limit (:obj:`int`, optional): Количество элементов, ``-1`` означает «до конца».
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    offset: Optional[int] = None
    limit: Optional[int] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.offset, self.limit)
