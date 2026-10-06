from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, Lyrics, VideoSupplement


@model
class Supplement(YandexMusicModel):
    """Класс, представляющий дополнительную информацию о треке.

    Warning:
        Получение текста из дополнительной информации устарело. Используйте
        :func:`yandex_music.Client.tracks_lyrics`.

    Attributes:
        id (:obj:`int`): Уникальный идентификатор дополнительной информации.
        lyrics (:obj:`yandex_music.Lyrics`): Текст песни.
        videos (:obj:`yandex_music.VideoSupplement`): Видео.
        radio_is_available (:obj:`bool`, optional): Доступно ли радио.
        description (:obj:`str`, optional): Полное описание эпизода подкаста.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    id: int
    lyrics: Optional['Lyrics']
    videos: List['VideoSupplement']
    radio_is_available: Optional[bool] = None
    description: Optional[str] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.id, self.lyrics, self.videos)
