from yandex_music import YandexMusicObject

class Supplement(YandexMusicObject):
    """Класс, представляющий дополнительную информацию о треке.

    Attributes:
        lyrics (:obj:`yandex_music.Lyrics`): Объект класса `yandex_music.Lyrics` представляющий текст песни
        videos (:obj:`yandex_music.VideoSupplement`): Объект класса `yandex_music.VideoSupplement` представляющий
            видео
        client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
            Music.

    Args:
        lyrics (:obj:`yandex_music.Lyrics`): Объект класса `yandex_music.Lyrics` представляющий текст песни
        videos (:obj:`yandex_music.VideoSupplement`): Объект класса `yandex_music.VideoSupplement` представляющий
            видео
        client (:obj:`yandex_music.Client`, optional): Объект класса :class:`yandex_music.Client` представляющий клиент
            Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """
    def __init__(self,
                 lyrics,
                 videos,
                 client=None,
                 **kwargs):
        self.lyrics = lyrics
        self.videos = videos

        self.client = client

    @classmethod
    def de_json(cls, data, client):
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
                Music.

        Returns:
            :obj:`yandex_music.Supplement`: Объект класса :class:`yandex_music.Supplement`.
        """
        if not data:
            return None
        
        data = super(Supplement, cls).de_json(data, client)
        from yandex_music import Lyrics, VideoSupplement
        data['lyrics'] = Lyrics.de_json(data.get('lyrics'), client) if 'lyrics' in data else None
        data['videos'] = VideoSupplement.de_list(data.get('videos'), client) if 'videos' in data else None

        return cls(client=client, **data)
