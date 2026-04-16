from dataclasses import field
from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Artist, ClientType, JSONType, Track


@model
class MetatagArtistEntry(YandexMusicModel):
    """Класс, представляющий запись артиста в списке метатега.

    Attributes:
        artist (:obj:`yandex_music.Artist`, optional): Артист.
        popular_tracks (:obj:`list` из :obj:`yandex_music.Track`): Популярные треки артиста.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    artist: Optional['Artist'] = None
    popular_tracks: List['Track'] = field(default_factory=list)
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.artist,)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['MetatagArtistEntry']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.MetatagArtistEntry`: Запись артиста в списке метатега.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music import Artist, Track

        cls_data['artist'] = Artist.de_json(cls_data.get('artist'), client)
        cls_data['popular_tracks'] = Track.de_list(cls_data.get('popular_tracks'), client)

        return cls(client=client, **cls_data)
