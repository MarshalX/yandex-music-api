from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicObject, ChartInfoMenuItem
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client


@model
class ChartInfoMenu(YandexMusicObject):
    """Класс, представляющий меню чарта.

    Attributes:
        items (:obj:`list` из :obj:`yandex_music.ChartInfoMenuItem`): Список элементов меню.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    items: List['ChartInfoMenuItem']
    client: Optional['Client'] = None

    def __post_init__(self):
        self._id_attrs = (self.items,)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['ChartInfoMenu']:
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

        return cls(client=client, **data)
