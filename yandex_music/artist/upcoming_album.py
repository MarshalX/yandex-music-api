from dataclasses import field
from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Artist, ClientType, ContentRestrictions


@model
class UpcomingAlbum(YandexMusicModel):
    """Класс, представляющий предстоящий релиз артиста.

    Attributes:
        id (:obj:`int`, optional): Уникальный идентификатор альбома.
        title (:obj:`str`, optional): Название альбома.
        type (:obj:`str`, optional): Тип альбома.
        release_date (:obj:`str`, optional): Дата выхода в формате ISO 8601.
        milliseconds_until_release (:obj:`int`, optional): Время до выхода в миллисекундах.
        cover_uri (:obj:`str`, optional): Ссылка на обложку.
        presaved (:obj:`bool`, optional): Сохранён ли релиз заранее (пресейв).
        artists (:obj:`list` из :obj:`yandex_music.Artist`): Исполнители.
        content_restrictions (:obj:`yandex_music.ContentRestrictions`, optional): Ограничения контента.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    id: Optional[int] = None
    title: Optional[str] = None
    type: Optional[str] = None
    release_date: Optional[str] = None
    milliseconds_until_release: Optional[int] = None
    cover_uri: Optional[str] = None
    presaved: Optional[bool] = None
    artists: List['Artist'] = field(default_factory=list)
    content_restrictions: Optional['ContentRestrictions'] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.id,)
