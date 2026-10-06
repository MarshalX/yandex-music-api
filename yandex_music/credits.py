from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType
    from yandex_music.credit import Credit


@model
class Credits(YandexMusicModel):
    """Класс, представляющий список участников создания контента (трека, клипа и т.д.).

    Attributes:
        credits (:obj:`list` из :obj:`yandex_music.Credit`, optional): Список участников.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    credits: Optional[List['Credit']] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.credits,)
