from yandex_music import YandexMusicObject


class VideoSupplement(YandexMusicObject):
    """Класс, представляющий видеоклипы.

    Attributes:
        cover (:obj:`str`): URL на обложку видео.
        title (:obj:`str`): Название видео.
        provider (:obj:`str`): Сервис поставляющий видео.
        provider_video_id (:obj:`str`): Уникальный идентификатор видео на сервисе.
        url (:obj:`str`): URL на видео.
        embed_url (:obj:`str`): URL на видео, находящегося на серверах Яндекса.
        embed (:obj:`str`): HTML тег для встраивания видео.
        client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
            Music.

    Args:
        cover (:obj:`str`): URL на обложку видео.
        title (:obj:`str`): Название видео.
        provider (:obj:`str`): Сервис поставляющий видео.
        provider_video_id (:obj:`str`): Уникальный идентификатор видео на сервисе.
        url (:obj:`str`): URL на видео.
        embed_url (:obj:`str`): URL на видео, находящегося на серверах Яндекса.
        embed (:obj:`str`): HTML тег для встраивания видео.
        client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
            Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 cover,
                 title,
                 provider,
                 provider_video_id,
                 url=None,
                 embed_url=None,
                 embed=None,
                 client=None,
                 **kwargs):
        self.cover = cover
        self.title = title
        self.provider = provider
        self.provider_video_id = provider_video_id

        self.url = url
        self.embed_url = embed_url
        self.embed = embed

        self.client = client
        self._id_attrs = (self.cover, self.title, self.provider_video_id)

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
