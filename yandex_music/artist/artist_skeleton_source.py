from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType


@model
class ArtistSkeletonSource(YandexMusicModel):
    """Класс, представляющий источник данных блока скелетона артиста.

    Attributes:
        uri (:obj:`str`, optional): URI для загрузки данных блока.
        count_web (:obj:`int`, optional): Количество элементов для веб-версии.
        count (:obj:`int`, optional): Количество элементов.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    uri: Optional[str] = None
    count_web: Optional[int] = None
    count: Optional[int] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.uri,)
