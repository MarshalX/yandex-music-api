from typing import TYPE_CHECKING, Any, List, Optional, Union

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, Playlist


@model
class PlaylistId(YandexMusicModel):
    """Класс, представляющий уникальный идентификатор плейлиста.

    Attributes:
        uid (:obj:`int`): Уникальный идентификатор пользователя владеющим плейлистом.
        kind (:obj:`int`): Уникальный идентификатор плейлиста.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    uid: int
    kind: int
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.uid, self.kind)

    @property
    def playlist_id(self) -> str:
        """Полный ID плейлиста."""
        return f'{self.uid}:{self.kind}'

    def fetch_playlist(self, *args: Any, **kwargs: Any) -> Optional[Union['Playlist', List['Playlist']]]:
        """Сокращение для::

        client.users_playlists(kind, uid, *args, **kwargs)
        """
        assert self.valid_client(self.client)
        return self.client.users_playlists(self.kind, self.uid, *args, **kwargs)

    async def fetch_playlist_async(self, *args: Any, **kwargs: Any) -> Optional[Union['Playlist', List['Playlist']]]:
        """Сокращение для::

        await client.users_playlists(kind, uid, *args, **kwargs)
        """
        assert self.valid_async_client(self.client)
        return await self.client.users_playlists(self.kind, self.uid, *args, **kwargs)

    # camelCase псевдонимы

    #: Псевдоним для :attr:`playlist_id`
    playlistId = playlist_id
    #: Псевдоним для :attr:`fetch_playlist`
    fetchPlaylist = fetch_playlist
    #: Псевдоним для :attr:`fetch_playlist_async`
    fetchPlaylistAsync = fetch_playlist_async
