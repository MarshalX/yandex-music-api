from typing import TYPE_CHECKING, Optional, List

from yandex_music import YandexMusicObject
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client


@model
class PlaylistId(YandexMusicObject):
    """Класс, представляющий уникальный идентификатор плейлиста.

    Attributes:
        uid (:obj:`int`): Уникальный идентификатор пользователя владеющим плейлистом.
        kind (:obj:`int`): Уникальный идентификатор плейлиста.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    uid: int
    kind: int
    client: Optional['Client'] = None

    def __post_init__(self):
        self._id_attrs = (self.uid, self.kind)

    @property
    def playlist_id(self):
        return f'{self.uid}:{self.kind}'

    def fetch_playlist(self, *args, **kwargs):
        """Сокращение для::

        client.users_playlists(kind, uid, *args, **kwargs)
        """
        return self.client.users_playlists(self.kind, self.uid, *args, **kwargs)

    async def fetch_playlist_async(self, *args, **kwargs):
        """Сокращение для::

        await client.users_playlists(kind, uid, *args, **kwargs)
        """
        return await self.client.users_playlists(self.kind, self.uid, *args, **kwargs)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['PlaylistId']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.PlaylistId`: Уникальный идентификатор плейлиста.
        """
        if not data:
            return None

        data = super(PlaylistId, cls).de_json(data, client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data: dict, client: 'Client') -> List['PlaylistId']:
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.PlaylistId`: Уникальные идентификаторы плейлистов.
        """
        if not data:
            return []

        playlist_ids = list()
        for playlist_id in data:
            playlist_ids.append(cls.de_json(playlist_id, client))

        return playlist_ids

    # camelCase псевдонимы

    #: Псевдоним для :attr:`playlist_id`
    playlistId = playlist_id
    #: Псевдоним для :attr:`fetch_playlist`
    fetchPlaylist = fetch_playlist
    #: Псевдоним для :attr:`fetch_playlist_async`
    fetchPlaylistAsync = fetch_playlist_async
