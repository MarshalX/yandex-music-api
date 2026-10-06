from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType
    from yandex_music.artist.artist import Artist
    from yandex_music.artist.artist_donation_goal import ArtistDonationGoal


@model
class ArtistDonationData(YandexMusicModel):
    """Класс, представляющий данные доната артисту.

    Attributes:
        tip_url (:obj:`str`, optional): Ссылка на страницу доната.
        artist (:obj:`yandex_music.Artist`, optional): Артист.
        goal (:obj:`yandex_music.ArtistDonationGoal`, optional): Цель доната.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    tip_url: Optional[str] = None
    artist: Optional['Artist'] = None
    goal: Optional['ArtistDonationGoal'] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.tip_url,)
