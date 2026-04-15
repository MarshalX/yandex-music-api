from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType
    from yandex_music.playlist.playlist import Playlist


@model
class PlaylistsList(YandexMusicModel):
    """Класс, представляющий список плейлистов.

    Attributes:
        playlists (:obj:`list` из :obj:`yandex_music.Playlist`, optional): Список плейлистов.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    playlists: Optional[List['Playlist']] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.playlists,)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['PlaylistsList']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.PlaylistsList`: Список плейлистов.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music import Playlist

        cls_data['playlists'] = Playlist.de_list(cls_data.get('playlists'), client)

        return cls(client=client, **cls_data)
