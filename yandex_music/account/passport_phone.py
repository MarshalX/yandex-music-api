from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicObject
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client


@model
class PassportPhone(YandexMusicObject):
    """Класс, представляющий номер телефона пользователя.

    Attributes:
        phone (:obj:`str`): Номер телефона.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    phone: str
    client: Optional['Client'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.phone,)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['PassportPhone']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.PassportPhone`: Номер телефона пользователя.
        """
        if not cls.is_valid_model_data(data):
            return None

        data = super(PassportPhone, cls).de_json(data, client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data: list, client: 'Client') -> List['PassportPhone']:
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.PassportPhone`: Номера телефонов пользователя.
        """
        if not cls.is_valid_model_data(data, array=True):
            return []

        return [cls.de_json(phone, client) for phone in data]
