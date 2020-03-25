from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client


class Lyrics(YandexMusicObject):
    """Класс, представляющий текст трека.

    Attributes:
        id (:obj:`int`): Уникальный идентификатор текста трека.
        lyrics (:obj:`str`): Первые строки текст песни.
        has_rights (:obj:`bool`): Есть ли права.
        full_lyrics (:obj:`str`): Текст песни.
        text_language (:obj:`str`): Язык текста.
        show_translation (:obj:`bool`): Показывать ли перевод.
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.

    Args:
        id_ (:obj:`int`): Уникальный идентификатор текста трека.
        lyrics (:obj:`str`): Первые строки текст песни.
        has_rights (:obj:`bool`): Есть ли права.
        full_lyrics (:obj:`str`): Текст песни.
        text_language (:obj:`str`): Язык песни.
        show_translation (:obj:`bool`): Показывать ли перевод.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 id_: int,
                 lyrics: str,
                 full_lyrics: str,
                 has_rights: bool,
                 text_language: str,
                 show_translation: bool,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        super().handle_unknown_kwargs(self, **kwargs)

        self.id = id_
        self.lyrics = lyrics
        self.full_lyrics = full_lyrics
        self.has_rights = has_rights
        self.text_language = text_language
        self.show_translation = show_translation

        self.client = client
        self._id_attrs = (self.id, self.lyrics, self.full_lyrics, self.has_rights,
                          self.text_language, self.show_translation)

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
