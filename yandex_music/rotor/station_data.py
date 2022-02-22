from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicObject
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client


@model
class StationData(YandexMusicObject):
    """Класс, представляющий информацию о личной станции.

    Attributes:
        name (:obj:`str`): Название станции.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    name: str
    client: Optional['Client'] = None

    def __post_init__(self):
        self._id_attrs = (self.name,)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['StationData']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.StationData`: Информация о личной станции.
        """
        if not data:
            return None

        data = super(StationData, cls).de_json(data, client)

        return cls(client=client, **data)
