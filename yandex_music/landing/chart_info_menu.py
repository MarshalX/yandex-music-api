from typing import TYPE_CHECKING, List, Optional

from yandex_music import ChartInfoMenuItem, JSONType, YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType


@model
class ChartInfoMenu(YandexMusicModel):
    """Класс, представляющий меню чарта.

    Attributes:
        items (:obj:`list` из :obj:`yandex_music.ChartInfoMenuItem`): Список элементов меню.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    items: List['ChartInfoMenuItem']
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.items,)

    @classmethod
    def de_json(cls, data: JSONType, client: 'ClientType') -> Optional['ChartInfoMenu']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.ChartInfoMenu`: Меню чарта.
        """
        if not cls.is_dict_model_data(data):
            return None

        data = cls.cleanup_data(data, client)
        data['items'] = ChartInfoMenuItem.de_list(data.get('items'), client)

        return cls(client=client, **data)
