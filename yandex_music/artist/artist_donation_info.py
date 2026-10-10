from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType


@model
class ArtistDonationInfo(YandexMusicModel):
    """Класс, представляющий ссылку на донат артисту.

    Attributes:
        title (:obj:`str`, optional): Текст ссылки.
        url (:obj:`str`, optional): URL страницы доната.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    title: Optional[str] = None
    url: Optional[str] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.title, self.url)
