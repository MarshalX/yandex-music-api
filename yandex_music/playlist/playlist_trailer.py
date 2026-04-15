from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType
    from yandex_music.playlist.playlist import Playlist
    from yandex_music.trailer_info import TrailerInfo


@model
class PlaylistTrailer(YandexMusicModel):
    """Класс, представляющий трейлер плейлиста.

    Attributes:
        playlist (:obj:`yandex_music.Playlist`, optional): Плейлист.
        trailer (:obj:`yandex_music.TrailerInfo`, optional): Информация о трейлере.
        shareable (:obj:`bool`, optional): Можно ли поделиться трейлером.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    playlist: Optional['Playlist'] = None
    trailer: Optional['TrailerInfo'] = None
    shareable: Optional[bool] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.playlist, self.trailer)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['PlaylistTrailer']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.PlaylistTrailer`: Трейлер плейлиста.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music import Playlist
        from yandex_music.trailer_info import TrailerInfo

        cls_data['playlist'] = Playlist.de_json(cls_data.get('playlist'), client)
        cls_data['trailer'] = TrailerInfo.de_json(cls_data.get('trailer'), client)

        return cls(client=client, **cls_data)
