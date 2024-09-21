from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType


@model
class LyricsInfo(YandexMusicModel):
    """Класс, описывающий доступные тексты трека.

    Attributes:
        has_available_sync_lyrics (:obj:`bool`): Наличие синхронизированного текста.
        has_available_text_lyrics (:obj:`bool`): Наличие текста трека.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    has_available_sync_lyrics: bool
    has_available_text_lyrics: bool
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.has_available_sync_lyrics, self.has_available_text_lyrics)
