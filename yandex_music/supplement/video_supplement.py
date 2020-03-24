from typing import TYPE_CHECKING, Optional, List

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client


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
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.

    Args:
        cover (:obj:`str`): URL на обложку видео.
        title (:obj:`str`): Название видео.
        provider (:obj:`str`): Сервис поставляющий видео.
        provider_video_id (:obj:`str`): Уникальный идентификатор видео на сервисе.
        url (:obj:`str`): URL на видео.
        embed_url (:obj:`str`): URL на видео, находящегося на серверах Яндекса.
        embed (:obj:`str`): HTML тег для встраивания видео.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 cover: str,
                 title: str,
                 provider: str,
                 provider_video_id: str,
                 url: Optional[str] = None,
                 embed_url: Optional[str] = None,
                 embed: Optional[str] = None,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        super().handle_unknown_kwargs(self, **kwargs)

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
    def de_json(cls, data: dict, client: 'Client') -> Optional['VideoSupplement']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.VideoSupplement`: Видеоклип.
        """
        if not data:
            return None

        data = super(VideoSupplement, cls).de_json(data, client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data: dict, client: 'Client') -> List['VideoSupplement']:
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.VideoSupplement`: Видеоклипы.
        """
        if not data:
            return []

        videos = list()
        for video in data:
            videos.append(cls.de_json(video, client))

        return videos
