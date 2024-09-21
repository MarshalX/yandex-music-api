from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType


@model
class Lyrics(YandexMusicModel):
    """Класс, представляющий текст трека.

    Warning:
        Получение текста из дополнительной информации устарело. Используйте
        :func:`yandex_music.Client.tracks_lyrics`.

    Attributes:
        id (:obj:`int`): Уникальный идентификатор текста трека.
        lyrics (:obj:`str`): Первые строки текст песни.
        has_rights (:obj:`bool`): Есть ли права.
        full_lyrics (:obj:`str`): Текст песни.
        show_translation (:obj:`bool`): Доступен ли перевод.
        text_language (:obj:`str`, optional): Язык песни.
        url (:obj:`str`, optional): Ссылка на источник перевода. Обычно genius.com.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    id: int
    lyrics: str
    full_lyrics: str
    has_rights: bool
    show_translation: bool
    text_language: Optional[str] = None
    url: Optional[str] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (
            self.id,
            self.lyrics,
            self.full_lyrics,
            self.has_rights,
            self.text_language,
            self.show_translation,
        )
