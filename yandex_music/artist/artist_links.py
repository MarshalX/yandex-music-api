from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType
    from yandex_music.artist.artist_link import ArtistLink


@model
class ArtistLinks(YandexMusicModel):
    """Класс, представляющий ссылки на страницы артиста.

    Attributes:
        links (:obj:`list` из :obj:`yandex_music.ArtistLink`, optional): Список ссылок.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    links: Optional[List['ArtistLink']] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.links,)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['ArtistLinks']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.ArtistLinks`: Ссылки на страницы артиста.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music import ArtistLink

        cls_data['links'] = ArtistLink.de_list(cls_data.get('links'), client)

        return cls(client=client, **cls_data)
