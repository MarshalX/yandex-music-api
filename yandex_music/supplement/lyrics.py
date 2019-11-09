from yandex_music import YandexMusicObject


class Lyrics(YandexMusicObject):
    """Класс, представляющий текст трека.

    Attributes:
        id (:obj:`int`): Уникальный идентификатор текста трека.
        lyrics (:obj:`str`): Первые строки текст песни.
        has_rights (:obj:`bool`): Есть ли права.
        full_lyrics (:obj:`str`): Текст песни.
        text_language (:obj:`str`): Язык текста.
        show_translation (:obj:`bool`): Показывать ли перевод.
        client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
            Music.

    Args:
        id (:obj:`int`): Уникальный идентификатор текста трека.
        lyrics (:obj:`str`): Первые строки текст песни.
        has_rights (:obj:`bool`): Есть ли права.
        full_lyrics (:obj:`str`): Текст песни.
        text_language (:obj:`str`): Язык песни.
        show_translation (:obj:`bool`): Показывать ли перевод.
        client (:obj:`yandex_music.Client`, optional): Объект класса :class:`yandex_music.Client` представляющий клиент
            Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 id,
                 lyrics,
                 full_lyrics,
                 has_rights,
                 text_language,
                 show_translation,
                 client=None,
                 **kwargs):
        self.id = id
        self.lyrics = lyrics
        self.full_lyrics = full_lyrics
        self.has_rights = has_rights
        self.text_language = text_language
        self.show_translation = show_translation

        self.client = client
        self._id_attrs = (self.id, self.lyrics, self.full_lyrics, self.has_rights,
                          self.text_language, self.show_translation)

    @classmethod
    def de_json(cls, data, client):
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
                Music.

        Returns:
            :obj:`yandex_music.Lyrics`: Объект класса :class:`yandex_music.Lyrics`.
        """
        if not data:
            return None
        
        data = super(Lyrics, cls).de_json(data, client)

        return cls(client=client, **data)
