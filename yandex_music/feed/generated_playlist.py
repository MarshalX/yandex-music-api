from typing import TYPE_CHECKING, Optional

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
    description: Optional[list] = None
    preview_description: Optional[str] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.type, self.ready, self.notify, self.data)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['GeneratedPlaylist']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.GeneratedPlaylist`: Автоматически сгенерированный плейлист.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music import Playlist

        cls_data['data'] = Playlist.de_json(data.get('data'), client)

        return cls(client=client, **cls_data)  # type: ignore
