from typing import TYPE_CHECKING, List, Optional, Union

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType


@model
class Video(YandexMusicModel):
    """Класс, представляющий видео.

    Attributes:
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
    """

    title: str
    cover: Optional[str] = None
    embed_url: Optional[str] = None
    provider: Optional[str] = None
    provider_video_id: Optional[Union[int, str]] = None
    youtube_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    duration: Optional[int] = None
    text: Optional[str] = None
    html_auto_play_video_player: Optional[str] = None
    regions: Optional[List[str]] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.provider_video_id, self.youtube_url, self.title)
