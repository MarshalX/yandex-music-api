from typing import TYPE_CHECKING, Optional, List

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client


class ChartInfoMenuItem(YandexMusicObject):
    """Класс, представляющий элемент меню чарта.

    Attributes:
        title (:obj:`str`): Заголовок.
        url (:obj:`str`): Постфикс для запроса чарта.
        selected (:obj:`bool`): Текущий ли элемент.

    Args:
        title (:obj:`str`): Заголовок.
        url (:obj:`str`): Постфикс для запроса чарта.
        selected (:obj:`bool`, optional): Текущий ли элемент.
    """

    def __init__(self, title: str, url: str, selected: Optional[bool] = False):
        self.title = title
        self.url = url
        self.selected = selected
        self._id_attrs = (url, selected)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> 'ChartInfoMenuItem':
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

        return cls(**data)

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
