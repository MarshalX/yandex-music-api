from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType, Value


@model
class DiscreteScale(YandexMusicModel):
    """Класс, представляющий дискретное значение.

    Note:
        Известные значения поля `type`: `discrete-scale`.

    Attributes:
        type (:obj:`str`): Тип.
        name (:obj:`str`): Название.
        min (:obj:`yandex_music.Value`): Минимальное значение.
        max (:obj:`yandex_music.Value`): Максимальное значение.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    type: str
    name: str
    min: Optional['Value']
    max: Optional['Value']
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.type, self.name, self.min, self.max)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['DiscreteScale']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.DiscreteScale`: Дискретное значение.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music import Value

        cls_data['min'] = Value.de_json(data.get('min'), client)
        cls_data['max'] = Value.de_json(data.get('max'), client)

        return cls(client=client, **cls_data)  # type: ignore
