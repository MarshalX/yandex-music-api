from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType
    from yandex_music.artist.artist_donation_item import ArtistDonationItem


@model
class ArtistDonations(YandexMusicModel):
    """Класс, представляющий блок донатов артиста.

    Attributes:
        donations (:obj:`list` из :obj:`yandex_music.ArtistDonationItem`, optional): Список донатов.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    donations: Optional[List['ArtistDonationItem']] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.donations,)
