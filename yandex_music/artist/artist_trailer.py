from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType
    from yandex_music.album.trailer_info import TrailerInfo
    from yandex_music.artist.artist import Artist


@model
class ArtistTrailer(YandexMusicModel):
    """Класс, представляющий трейлер артиста.

    Attributes:
        artist (:obj:`yandex_music.Artist`, optional): Артист.
        trailer (:obj:`yandex_music.TrailerInfo`, optional): Информация о трейлере.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    artist: Optional['Artist'] = None
    trailer: Optional['TrailerInfo'] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.artist, self.trailer)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['ArtistTrailer']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.ArtistTrailer`: Трейлер артиста.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music import Artist
        from yandex_music.album.trailer_info import TrailerInfo

        cls_data['artist'] = Artist.de_json(cls_data.get('artist'), client)
        cls_data['trailer'] = TrailerInfo.de_json(cls_data.get('trailer'), client)

        return cls(client=client, **cls_data)
