from dataclasses import field
from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType
    from yandex_music.concert.concert import Concert


@model
class ArtistConcerts(YandexMusicModel):
    """Класс, представляющий список концертов артиста.

    Attributes:
        artist_title (:obj:`str`, optional): Название артиста.
        concerts (:obj:`list` из :obj:`yandex_music.Concert`): Список концертов.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    artist_title: Optional[str] = None
    concerts: List['Concert'] = field(default_factory=list)
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.artist_title, self.concerts)
