from typing import TYPE_CHECKING, Optional, List

from yandex_music import YandexMusicObject
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client


@model
class VideoSupplement(YandexMusicObject):
    """Класс, представляющий видеоклипы.

    Attributes:
        cover (:obj:`str`): URL на обложку видео.
        provider (:obj:`str`): Сервис поставляющий видео.
        title (:obj:`str`, optional): Название видео.
        provider_video_id (:obj:`str`, optional): Уникальный идентификатор видео на сервисе.
        url (:obj:`str`, optional): URL на видео.
        embed_url (:obj:`str`, optional): URL на видео, находящегося на серверах Яндекса.
        embed (:obj:`str`, optional): HTML тег для встраивания видео.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    cover: str
    provider: str
    title: Optional[str] = None
    provider_video_id: Optional[str] = None
    url: Optional[str] = None
    embed_url: Optional[str] = None
    embed: Optional[str] = None
    client: Optional['Client'] = None

    def __post_init__(self):
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
