from dataclasses import field
from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType
    from yandex_music.concert.concert_location import ConcertLocation


@model
class ConcertLocations(YandexMusicModel):
    """Класс, представляющий список местоположений для фильтрации концертов.

    Attributes:
        locations (:obj:`list` из :obj:`yandex_music.ConcertLocation`): Список местоположений.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    locations: List['ConcertLocation'] = field(default_factory=list)
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.locations,)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['ConcertLocations']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.ConcertLocations`: Список местоположений.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music.concert.concert_location import ConcertLocation

        cls_data['locations'] = ConcertLocation.de_list(cls_data.get('locations'), client)

        return cls(client=client, **cls_data)
