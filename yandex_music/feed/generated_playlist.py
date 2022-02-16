from typing import TYPE_CHECKING, Optional, List

from yandex_music import YandexMusicObject
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client, Playlist


@model
class GeneratedPlaylist(YandexMusicObject):
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
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    type: str
    ready: bool
    notify: bool
    data: Optional['Playlist']
    description: Optional[list] = None
    client: Optional['Client'] = None

    def __post_init__(self):
        self._id_attrs = (self.type, self.ready, self.notify, self.data)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['GeneratedPlaylist']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.GeneratedPlaylist`: Автоматически сгенерированный плейлист.
        """
        if not data:
            return None

        data = super(GeneratedPlaylist, cls).de_json(data, client)
        from yandex_music import Playlist

        data['data'] = Playlist.de_json(data.get('data'), client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data: dict, client: 'Client') -> List['GeneratedPlaylist']:
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.GeneratedPlaylist`: Автоматически сгенерированные плейлисты.
        """
        if not data:
            return []

        return [cls.de_json(generated_playlist, client) for generated_playlist in data]
