from typing import TYPE_CHECKING, Optional, List

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client, Playlist


class GeneratedPlaylist(YandexMusicObject):
    """Класс, представляющий автоматически сгенерированный плейлист.

    Note:
        Известные значения `type`: `playlistOfTheDay`, `origin`, `recentTracks`, `neverHeard`, `podcasts`,
        `missedLikes`.

    Attributes:
        type (:obj:`str`): Тип сгенерированного плейлиста.
        ready (:obj:`bool`): Готовность плейлиста.
        notify (:obj:`bool`): Уведомлён ли пользователь об обновлении содержания.
        data (:obj:`yandex_music.Playlist`): Сгенерированный плейлист.
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.

    Args:
        type_ (:obj:`str`): Тип сгенерированного плейлиста.
        ready (:obj:`bool`): Готовность плейлиста.
        notify (:obj:`bool`): Уведомлён ли пользователь об обновлении содержания.
        data (:obj:`yandex_music.Playlist`, optional): Сгенерированный плейлист.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 type_: str,
                 ready: bool,
                 notify: bool,
                 data: Optional['Playlist'],
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        super().handle_unknown_kwargs(self, **kwargs)

        self.type = type_
        self.ready = ready
        self.notify = notify
        self.data = data

        self.client = client
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

        generated_playlists = list()
        for generated_playlist in data:
            generated_playlists.append(cls.de_json(generated_playlist, client))

        return generated_playlists
