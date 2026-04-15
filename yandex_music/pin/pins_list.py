from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType
    from yandex_music.pin.pin import Pin


@model
class PinsList(YandexMusicModel):
    """Класс, представляющий список закреплённых элементов.

    Attributes:
        pins (:obj:`list` из :obj:`yandex_music.Pin`, optional): Список закреплённых элементов.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    pins: Optional[List['Pin']] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.pins,)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['PinsList']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.PinsList`: Список закреплённых элементов.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music import Pin

        cls_data['pins'] = Pin.de_list(cls_data.get('pins'), client)

        return cls(client=client, **cls_data)
