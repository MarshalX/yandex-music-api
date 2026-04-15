from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType
    from yandex_music.artist.artist import Artist
    from yandex_music.artist.artist_link import ArtistLink
    from yandex_music.artist.stats import Stats
    from yandex_music.cover import Cover


@model
class ArtistAbout(YandexMusicModel):
    """Класс, представляющий информацию «Об артисте».

    Attributes:
        artist (:obj:`yandex_music.Artist`, optional): Артист.
        stats (:obj:`yandex_music.Stats`, optional): Статистика прослушиваний.
        description (:obj:`str`, optional): Текстовое описание артиста.
        links (:obj:`list` из :obj:`yandex_music.ArtistLink`, optional): Ссылки на внешние ресурсы.
        covers (:obj:`list` из :obj:`yandex_music.Cover`, optional): Список обложек артиста.
        artist_type (:obj:`str`, optional): Тип артиста.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    artist: Optional['Artist'] = None
    stats: Optional['Stats'] = None
    description: Optional[str] = None
    links: Optional[List['ArtistLink']] = None
    covers: Optional[List['Cover']] = None
    artist_type: Optional[str] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.artist,)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['ArtistAbout']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.ArtistAbout`: Информация «Об артисте».
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music import Artist, Cover
        from yandex_music.artist.artist_link import ArtistLink
        from yandex_music.artist.stats import Stats

        cls_data['artist'] = Artist.de_json(cls_data.get('artist'), client)
        cls_data['stats'] = Stats.de_json(cls_data.get('stats'), client)
        cls_data['links'] = ArtistLink.de_list(cls_data.get('links'), client)
        cls_data['covers'] = Cover.de_list(cls_data.get('covers'), client)

        return cls(client=client, **cls_data)
