from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicObject
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client


@model
class Lyrics(YandexMusicObject):
    """Класс, представляющий текст трека.

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
    client: Optional['Client'] = None

    def __post_init__(self):
        self._id_attrs = (
            self.id,
            self.lyrics,
            self.full_lyrics,
            self.has_rights,
            self.text_language,
            self.show_translation,
        )

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Lyrics']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Lyrics`: Текст трека.
        """
        if not data:
            return None

        data = super(Lyrics, cls).de_json(data, client)

        return cls(client=client, **data)
