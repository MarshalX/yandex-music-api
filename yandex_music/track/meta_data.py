from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client


@model
class MetaData(YandexMusicModel):
    """Класс, представляющий метаданные трека.

    Attributes:
        album (:obj:`str`, optional): Название альбома.
        volume (:obj:`int`, optional): Диск (раздел).
        year (:obj:`int`, optional): Год выхода.
        number (:obj:`int`, optional): Позиция в альбоме.
        genre (:obj:`str`, optional): Жанр.
        lyricist (:obj:`str`, optional): Текст песни. Есть только у пользовательских треков.
        version (:obj:`str`, optional): Версия TODO.
        composer (:obj:`str`, optional): Композитор TODO.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    album: Optional[str] = None
    volume: Optional[int] = None
    year: Optional[int] = None
    number: Optional[int] = None
    genre: Optional[str] = None
    lyricist: Optional[str] = None
    version: Optional[str] = None
    composer: Optional[str] = None
    client: Optional['Client'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.album, self.volume, self.year)
