from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType
    from yandex_music.pin.pin_data import PinData


@model
class Pin(YandexMusicModel):
    """Класс, представляющий закреплённый элемент.

    Note:
        Известные значения поля `type`: `artist_item`, `album_item`, `playlist_item`, `wave_item`.

    Attributes:
        type (:obj:`str`): Тип закреплённого элемента.
        data (:obj:`yandex_music.PinData`, optional): Данные закреплённого элемента.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    type: str
    data: Optional['PinData'] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.type, self.data)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['Pin']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Pin`: Закреплённый элемент.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music.pin.pin_data import PinData

        cls_data['data'] = PinData.de_json(cls_data.get('data'), client)

        return cls(client=client, **cls_data)
