from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType
    from yandex_music.artist.artist import Artist
    from yandex_music.artist.artist_trailer_status import ArtistTrailerStatus
    from yandex_music.artist.stats import Stats
    from yandex_music.cover import Cover


@model
class ArtistInfo(YandexMusicModel):
    """Класс, представляющий подробную информацию об артисте.

    Attributes:
        artist (:obj:`yandex_music.Artist`, optional): Артист.
        likes_count (:obj:`int`, optional): Количество лайков.
        stats (:obj:`yandex_music.Stats`, optional): Статистика прослушиваний.
        trailer (:obj:`yandex_music.ArtistTrailerStatus`, optional): Статус доступности трейлера.
        covers (:obj:`list` из :obj:`yandex_music.Cover`, optional): Список обложек артиста.
        description (:obj:`str`, optional): Текстовое описание артиста.
        artist_type (:obj:`str`, optional): Тип артиста.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    artist: Optional['Artist'] = None
    likes_count: Optional[int] = None
    stats: Optional['Stats'] = None
    trailer: Optional['ArtistTrailerStatus'] = None
    covers: Optional[List['Cover']] = None
    description: Optional[str] = None
    artist_type: Optional[str] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.artist,)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['ArtistInfo']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.ArtistInfo`: Подробная информация об артисте.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music import Artist, Cover
        from yandex_music.artist.artist_trailer_status import ArtistTrailerStatus
        from yandex_music.artist.stats import Stats

        cls_data['artist'] = Artist.de_json(cls_data.get('artist'), client)
        cls_data['stats'] = Stats.de_json(cls_data.get('stats'), client)
        cls_data['trailer'] = ArtistTrailerStatus.de_json(cls_data.get('trailer'), client)
        cls_data['covers'] = Cover.de_list(cls_data.get('covers'), client)

        return cls(client=client, **cls_data)
