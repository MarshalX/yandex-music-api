from typing import TYPE_CHECKING, List

from yandex_music import YandexMusicObject, ChartInfoMenuItem

if TYPE_CHECKING:
    from yandex_music import Client


class ChartInfoMenu(YandexMusicObject):
    """Класс, представляющий меню чарта.

    Attributes:
        items (:obj:`list` из :obj:`yandex_music.ChartInfoMenuItem): Список элементов меню.

    Args:
        items (:obj:`list` из :obj:`yandex_music.ChartInfoMenuItem): Список элементов меню.
    """

    def __init__(self, items: List['ChartInfoMenuItem']):
        self.items = items
        self._id_attrs = tuple(i.url for i in items)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> 'ChartInfoMenu':
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.ChartInfoMenu`: Меню чарта.
        """
        if not data:
            return None

        data = super(ChartInfoMenu, cls).de_json(data, client)
        data['items'] = ChartInfoMenuItem.de_list(data.get('items'), client)

        return cls(**data)
