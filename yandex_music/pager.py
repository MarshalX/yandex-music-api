from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType


@model
class Pager(YandexMusicModel):
    """Класс, представляющий пагинацию.

    Attributes:
        total (:obj:`int`): Всего треков.
        page (:obj:`int`): Номер страницы.
        per_page (:obj:`int`): Количество треков на странице.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    total: int
    page: int
    per_page: int
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.total, self.page, self.per_page)
