from typing import TYPE_CHECKING, Optional, List

from yandex_music import YandexMusicObject
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client


@model
class ChartInfoMenuItem(YandexMusicObject):
    """Класс, представляющий элемент меню чарта.

    Attributes:
        title (:obj:`str`): Заголовок.
        url (:obj:`str`): Постфикс для запроса чарта.
        selected (:obj:`bool`, optional): Текущий ли элемент.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    title: str
    url: str
    selected: Optional[bool] = None
    client: Optional['Client'] = None

    def __post_init__(self):
        self._id_attrs = (self.url, self.selected)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['ChartInfoMenuItem']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.ChartInfoMenuItem`: Элемент меню.
        """
        if not data:
            return None

        data = super(ChartInfoMenuItem, cls).de_json(data, client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data: list, client: 'Client') -> List['ChartInfoMenuItem']:
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.ChartInfoMenuItem`: Список элементов меню чарта.
        """
        if not data:
            return []

        return [cls.de_json(item, client) for item in data]
