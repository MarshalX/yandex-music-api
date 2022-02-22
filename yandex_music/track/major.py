from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicObject
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client


@model
class Major(YandexMusicObject):
    """Класс, представляющий мейджор-лейбл звукозаписи.

    Attributes:
        id (:obj:`int`): Уникальный идентификатор.
        name (:obj:`str`): Название.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    id: int
    name: str
    client: Optional['Client'] = None

    def __post_init__(self):
        self._id_attrs = (self.id, self.name)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Major']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Major`: Мейджор-лейбл звукозаписи.
        """
        if not data:
            return None

        data = super(Major, cls).de_json(data, client)

        return cls(client=client, **data)
