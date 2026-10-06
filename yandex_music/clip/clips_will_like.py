from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType
    from yandex_music.clip.clip import Clip
    from yandex_music.pager import Pager


@model
class ClipsWillLike(YandexMusicModel):
    """Класс, представляющий подборку рекомендуемых клипов.

    Attributes:
        clips (:obj:`list` из :obj:`yandex_music.Clip`, optional): Список клипов.
        pager (:obj:`yandex_music.Pager`, optional): Пагинация.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    clips: Optional[List['Clip']] = None
    pager: Optional['Pager'] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.clips, self.pager)
