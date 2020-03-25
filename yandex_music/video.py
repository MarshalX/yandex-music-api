from typing import TYPE_CHECKING, Optional, List, Union

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client


class Video(YandexMusicObject):
    """Класс, представляющий видео.

   Attributes:
        title (:obj:`str`): Название видео.
        cover (:obj:`str`): Ссылка на изображение.
        embed_url (:obj:`str`): Ссылка на видео.
        provider (:obj:`str`): Провайдер видео.
        provider_video_id (:obj:`int` | :obj:`str`): Идентификатор видео.
        youtube_url (:obj:`str`): Ссылка на видео Youtube.
        thumbnail_url (:obj:`str`): Ссылка на изображение.
        duration (:obj:`int`): Длительность видео в секундах.
        text (:obj:`str`): Текст.
        html_auto_play_video_player (:obj:`str`): HTML тег для встраивания в разметку страницы.
        regions (:obj:`list` из :obj:`str`): Регион TODO.
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.

   Args:
        title (:obj:`str`): Название видео.
        cover (:obj:`str`, optional): Ссылка на изображение.
        embed_url (:obj:`str`, optional): Ссылка на видео.
        provider (:obj:`str`, optional): Провайдер видео.
        provider_video_id (:obj:`int` | :obj:`str`, optional): Идентификатор видео.
        youtube_url (:obj:`str`, optional): Ссылка на видео Youtube.
        thumbnail_url (:obj:`str`, optional): Ссылка на изображение.
        duration (:obj:`int`, optional): Длительность видео в секундах.
        text (:obj:`str`, optional): Текст.
        html_auto_play_video_player (:obj:`str`, optional): HTML тег для встраивания в разметку страницы.
        regions (:obj:`list` из :obj:`str`, optional): Регион TODO.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
   """

    def __init__(self,
                 title: str,
                 cover: Optional[str] = None,
                 embed_url: Optional[str] = None,
                 provider: Optional[str] = None,
                 provider_video_id: Optional[Union[int, str]] = None,
                 youtube_url: Optional[str] = None,
                 thumbnail_url: Optional[str] = None,
                 duration: Optional[int] = None,
                 text: Optional[str] = None,
                 html_auto_play_video_player: Optional[str] = None,
                 regions: Optional[List[str]] = None,
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
            client (:obj:`yandex_music.Client`): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Video`: Видео.
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
            client (:obj:`yandex_music.Client`): Клиент Yandex Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.Video`: Видео.
        """
        if not data:
            return []

        videos = list()
        for video in data:
            videos.append(cls.de_json(video, client))

        return videos
