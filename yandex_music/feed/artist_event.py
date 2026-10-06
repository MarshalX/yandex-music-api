from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Artist, ClientType, Track


@model
class ArtistEvent(YandexMusicModel):
    """Класс, представляющий артиста в событии фида.

    Attributes:
        artist (:obj:`yandex_music.Artist`, optional): Артист.
        tracks (:obj:`list` из :obj:`yandex_music.Track`): Треки.
        similar_to_artists_from_history (:obj:`list` из :obj:`yandex_music.Artist`): Похожие артисты из истории.
        subscribed (:obj:`bool`): Подписан ли на событие.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    artist: Optional['Artist']
    tracks: List['Track']
    similar_to_artists_from_history: List['Artist']
    subscribed: Optional['bool'] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.artist, self.tracks, self.similar_to_artists_from_history)
