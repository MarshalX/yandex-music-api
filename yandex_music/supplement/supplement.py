from yandex_music import YandexMusicObject


class Supplement(YandexMusicObject):
    """Класс, представляющий дополнительную информацию о треке.

    Attributes:
        id (:obj:`int`): Уникальный идентификатор дополнительной информации.
        lyrics (:obj:`yandex_music.Lyrics`): Объект класса :class:`yandex_music.Lyrics` представляющий текст песни.
        videos (:obj:`yandex_music.VideoSupplement`): Объект класса :class:`yandex_music.VideoSupplement` представляющий
            видео.
        radio_is_available (:obj:`bool`): Доступно ли радио.
        client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
            Music.

    Args:
        id (:obj:`int`): Уникальный идентификатор дополнительной информации.
        lyrics (:obj:`yandex_music.Lyrics`): Объект класса :class:`yandex_music.Lyrics` представляющий текст песни.
        videos (:obj:`yandex_music.VideoSupplement`): Объект класса :class:`yandex_music.VideoSupplement` представляющий
            видео.
        radio_is_available (:obj:`bool`): Доступно ли радио.
        client (:obj:`yandex_music.Client`, optional): Объект класса :class:`yandex_music.Client` представляющий клиент
            Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 id,
                 lyrics,
                 videos,
                 radio_is_available,
                 client=None,
                 **kwargs):
        self.id = id
        self.lyrics = lyrics
        self.videos = videos
        self.radio_is_available = radio_is_available

        self.client = client
        self._id_attrs = (self.id, self.lyrics, self.videos, self.radio_is_available)

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
        data['lyrics'] = Lyrics.de_json(data.get('lyrics'), client)
        data['videos'] = VideoSupplement.de_list(data.get('videos'), client)

        return cls(client=client, **data)
