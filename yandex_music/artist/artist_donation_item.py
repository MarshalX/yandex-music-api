from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType
    from yandex_music.artist.artist_donation_data import ArtistDonationData


@model
class ArtistDonationItem(YandexMusicModel):
    """Класс, представляющий элемент блока донатов артиста.

    Note:
        Известные значения поля ``type``: ``donation_item``.

    Attributes:
        type (:obj:`str`, optional): Тип элемента.
        data (:obj:`yandex_music.ArtistDonationData`, optional): Данные доната.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    type: Optional[str] = None
    data: Optional['ArtistDonationData'] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.type, self.data)
