from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client


@model
class VideoSupplement(YandexMusicModel):
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

    def __post_init__(self) -> None:
        self._id_attrs = (self.cover, self.title, self.provider_video_id)
