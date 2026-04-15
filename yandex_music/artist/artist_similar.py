from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType
    from yandex_music.artist.artist import Artist


@model
class ArtistSimilar(YandexMusicModel):
    """Класс, представляющий похожих артистов.

    Attributes:
        artist (:obj:`yandex_music.Artist`, optional): Артист, для которого найдены похожие.
        similar_artists (:obj:`list` из :obj:`yandex_music.Artist`, optional): Список похожих артистов.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    artist: Optional['Artist'] = None
    similar_artists: Optional[List['Artist']] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.artist, self.similar_artists)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['ArtistSimilar']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.ArtistSimilar`: Похожие артисты.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music import Artist

        cls_data['artist'] = Artist.de_json(cls_data.get('artist'), client)
        cls_data['similar_artists'] = Artist.de_list(cls_data.get('similar_artists'), client)

        return cls(client=client, **cls_data)
