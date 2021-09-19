from typing import TYPE_CHECKING, Optional, List

from yandex_music import YandexMusicObject
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client


@model
class Value(YandexMusicObject):
    """Класс, представляющий значение(переменную).

    Attributes:
        value (:obj:`str`): Значение.
        name (:obj:`str`): Название.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    value: str
    name: str
    client: Optional['Client'] = None

    def __post_init__(self):
        self._id_attrs = (self.value, self.name)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Value']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Value`: Значение.
        """
        if not data:
            return None

        data = super(Value, cls).de_json(data, client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data: dict, client: 'Client') -> List['Value']:
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.Value`: Значения.
        """
        if not data:
            return []

        values = list()
        for value in data:
            values.append(cls.de_json(value, client))

        return values
