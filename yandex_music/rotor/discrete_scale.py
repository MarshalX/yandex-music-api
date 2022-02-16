from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicObject
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client, Value


@model
class DiscreteScale(YandexMusicObject):
    """Класс, представляющий дискретное значение.

    Note:
        Известные значения поля `type`: `discrete-scale`.

    Attributes:
        type (:obj:`str`): Тип.
        name (:obj:`str`): Название.
        min (:obj:`yandex_music.Value`): Минимальное значение.
        max (:obj:`yandex_music.Value`): Максимальное значение.
        client (:obj:`yandex_music.Client` optional): Клиент Yandex Music.
    """

    type: str
    name: str
    min: Optional['Value']
    max: Optional['Value']
    client: Optional['Client'] = None

    def __post_init__(self):
        self._id_attrs = (self.type, self.name, self.min, self.max)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['DiscreteScale']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.DiscreteScale`: Дискретное значение.
        """
        if not data:
            return None

        data = super(DiscreteScale, cls).de_json(data, client)
        from yandex_music import Value

        data['min'] = Value.de_json(data.get('min'), client)
        data['max'] = Value.de_json(data.get('max'), client)

        return cls(client=client, **data)
