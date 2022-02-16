from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicObject
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client


@model
class ShotType(YandexMusicObject):
    """Класс, представляющий тип шота от Алисы.

    Attributes:
        id (:obj:`str`): Уникальный идентификатор типа.
        title (:obj:`str`): Заголовок шота.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    id: str
    title: str
    client: Optional['Client'] = None

    def __post_init__(self):
        self._id_attrs = (self.id, self.title)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['ShotType']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.ShotType`: Тип шота от Алисы.
        """
        if not data:
            return None

        data = super(ShotType, cls).de_json(data, client)

        return cls(client=client, **data)
