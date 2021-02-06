from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicObject, ChartInfoMenuItem

if TYPE_CHECKING:
    from yandex_music import Client


class ChartInfoMenu(YandexMusicObject):
    """Класс, представляющий меню чарта.

    Attributes:
        items (:obj:`list` из :obj:`yandex_music.ChartInfoMenuItem`): Список элементов меню.
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.

    Args:
        items (:obj:`list` из :obj:`yandex_music.ChartInfoMenuItem`): Список элементов меню.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    def __init__(self, items: List['ChartInfoMenuItem'], client: Optional['Client'] = None, **kwargs):
        self.items = items

        self.client = client
        self._id_attrs = (self.items,)

        super().handle_unknown_kwargs(self, **kwargs)

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
