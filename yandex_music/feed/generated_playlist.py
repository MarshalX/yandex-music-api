from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType, Playlist


@model
class GeneratedPlaylist(YandexMusicModel):
    """Класс, представляющий автоматически сгенерированный плейлист.

    Note:
        Известные значения `type`: `playlistOfTheDay`, `origin`, `recentTracks`, `neverHeard`, `podcasts`,
        `missedLikes`.

    Attributes:
        type (:obj:`str`): Тип сгенерированного плейлиста.
        ready (:obj:`bool`): Готовность плейлиста.
        notify (:obj:`bool`): Уведомлён ли пользователь об обновлении содержания.
        data (:obj:`yandex_music.Playlist`, optional): Сгенерированный плейлист.
        description (:obj:`list`, optional): Описание TODO.
        preview_description (:obj:`str`, optional): Короткое описание под блоком лендинга.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    type: str
    ready: bool
    notify: bool
    data: Optional['Playlist']
    description: Optional[List['JSONType']] = None
    preview_description: Optional[str] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.type, self.ready, self.notify, self.data)
