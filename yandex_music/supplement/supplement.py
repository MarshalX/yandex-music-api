from typing import TYPE_CHECKING, Optional, List

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client, Lyrics, VideoSupplement


class Supplement(YandexMusicObject):
    """Класс, представляющий дополнительную информацию о треке.

    Attributes:
        id (:obj:`int`): Уникальный идентификатор дополнительной информации.
        lyrics (:obj:`yandex_music.Lyrics`): Текст песни.
        videos (:obj:`yandex_music.VideoSupplement`): Видео.
        radio_is_available (:obj:`bool`): Доступно ли радио.
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.

    Args:
        id_ (:obj:`int`): Уникальный идентификатор дополнительной информации.
        lyrics (:obj:`yandex_music.Lyrics`): Текст песни.
        videos (:obj:`yandex_music.VideoSupplement`): Видео.
        radio_is_available (:obj:`bool`): Доступно ли радио.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 id_: int,
                 lyrics: Optional['Lyrics'],
                 videos: List['VideoSupplement'],
                 radio_is_available: bool,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        super().handle_unknown_kwargs(self, **kwargs)

        self.id = id_
        self.lyrics = lyrics
        self.videos = videos
        self.radio_is_available = radio_is_available

        self.client = client
        self._id_attrs = (self.id, self.lyrics, self.videos, self.radio_is_available)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Supplement']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Supplement`: Дополнительная информация о треке.
        """
        if not data:
            return None

        data = super(Supplement, cls).de_json(data, client)
        from yandex_music import Lyrics, VideoSupplement
        data['lyrics'] = Lyrics.de_json(data.get('lyrics'), client)
        data['videos'] = VideoSupplement.de_list(data.get('videos'), client)

        return cls(client=client, **data)
