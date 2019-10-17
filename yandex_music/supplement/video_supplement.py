from yandex_music import YandexMusicObject

class VideoSupplement(YandexMusicObject):
    """Класс, представляющий видео-клипы

    Attributes:
        cover (:obj:`str`): URL на обложку видео
        title (:obj:`str`): Название видео
        url (:obj:`str`): URL на видео
        client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
            Music.

    Args:
        cover (:obj:`str`): URL на обложку видео
        title (:obj:`str`): Название видео
        url (:obj:`str`): URL на видео
        client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
            Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """
    def __init__(self,
                 cover,
                 title,
                 url,
                 client=None,
                 **kwargs):
        self.cover = cover
        self.title = title
        self.url = url

        self.client = client

    @classmethod
    def de_json(cls, data, client):
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
                Music.

        Returns:
            :obj:`yandex_music.VideoSupplement`: Объект класса :class:`yandex_music.VideoSupplement`.
        """
        if not data:
            return None

        data = super(VideoSupplement, cls).de_json(data, client)
        if 'url' not in data:
            data['url'] = data['embed_url']

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data, client):
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
                Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.VideoSupplement`: Список объектов класса :class:`yandex_music.VideoSupplement`.
        """
        if not data:
            return []

        videos = list()
        for video in data:
            videos.append(cls.de_json(video, client))

        return videos