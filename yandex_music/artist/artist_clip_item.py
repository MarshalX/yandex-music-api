from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType
    from yandex_music.artist.artist_clip_data import ArtistClipData


@model
class ArtistClipItem(YandexMusicModel):
    """Класс, представляющий элемент блока клипов артиста.

    Note:
        Известные значения поля ``type``: ``clip``.

    Attributes:
        type (:obj:`str`, optional): Тип элемента.
        data (:obj:`yandex_music.ArtistClipData`, optional): Данные клипа.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    type: Optional[str] = None
    data: Optional['ArtistClipData'] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.type, self.data)
