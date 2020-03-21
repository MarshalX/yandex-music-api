from typing import TYPE_CHECKING, Optional, List, Union

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client


class Video(YandexMusicObject):
    """Класс, представляющий .

    Attributes:
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

    Args:
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 title: str,
                 cover: Optional[str] = None,
                 embed_url: Optional[str] = None,
                 provider: Optional['str'] = None,
                 provider_video_id: Optional[Union[int, str]] = None,
                 youtube_url: Optional[str] = None,
                 thumbnail_url: Optional[str] = None,
                 duration=None,
                 text=None,
                 html_auto_play_video_player=None,
                 regions=None,
                 client: Optional['Client'] = None,
                 **kwargs):
        self.title = title

        # Видео из brief info
        self.cover = cover
        self.embed_url = embed_url
        self.provider = provider
        self.provider_video_id = provider_video_id

        # Видео из результатов поиска
        self.youtube_url = youtube_url
        self.thumbnail_url = thumbnail_url
        self.duration = duration
        self.text = text
        self.html_auto_play_video_player = html_auto_play_video_player
        self.regions = regions

        self.client = client
        self._id_attrs = (self.provider_video_id, self.youtube_url, self.title)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Video']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Video`: TODO.
        """
        if not data:
            return None

        data = super(Video, cls).de_json(data, client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data: dict, client: 'Client') -> List['Video']:
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.Video`: TODOqq.
        """
        if not data:
            return []

        videos = list()
        for video in data:
            videos.append(cls.de_json(video, client))

        return videos
