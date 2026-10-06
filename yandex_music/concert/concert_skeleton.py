from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, SkeletonBlock


@model
class ConcertSkeleton(YandexMusicModel):
    """Класс, представляющий скелетон страницы концерта.

    Attributes:
        id (:obj:`str`, optional): Идентификатор скелетона.
        title (:obj:`str`, optional): Заголовок скелетона.
        blocks (:obj:`list` из :obj:`yandex_music.SkeletonBlock`, optional): Блоки скелетона.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    id: Optional[str] = None
    title: Optional[str] = None
    blocks: Optional[List['SkeletonBlock']] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.id, self.title)
