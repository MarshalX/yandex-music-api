from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType


@model
class SkeletonViewAllAction(YandexMusicModel):
    """Класс, представляющий действие «Показать все» в блоке скелетона.

    Attributes:
        deeplink (:obj:`str`, optional): Диплинк для мобильного приложения.
        weblink (:obj:`str`, optional): Ссылка для веб-версии.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    deeplink: Optional[str] = None
    weblink: Optional[str] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.deeplink, self.weblink)
