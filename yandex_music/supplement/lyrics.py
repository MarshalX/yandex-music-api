from yandex_music import YandexMusicObject

class Lyrics(YandexMusicObject):
    """Класс, представляющий текст трека

    Attributes:
        full_lyrics (:obj:`str`): Текст песни
        text_language (:obj:`str`): Язык текста
        client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
            Music.

    Args:
        full_lyrics (:obj:`str`): Текст песни
        text_language (:obj:`str`): Язык песни
            видео
        client (:obj:`yandex_music.Client`, optional): Объект класса :class:`yandex_music.Client` представляющий клиент
            Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """
    def __init__(self,
                 full_lyrics,
                 text_language,
                 client=None,
                 **kwargs):
        self.full_lyrics = full_lyrics
        self.text_language = text_language

        self.client = client

    @classmethod
    def de_json(cls, data, client):
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
                Music.

        Returns:
            :obj:`yandex_music.Cover`: Объект класса :class:`yandex_music.Cover`.
        """
        if not data:
            return None
        
        data = super(Lyrics, cls).de_json(data, client)

        return cls(client=client, **data)


