from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client, Value


class DiscreteScale(YandexMusicObject):
    """Класс, представляющий дискретное значение.

    Note:
        Известные значения поля `type`: `discrete-scale`.

    Attributes:
        type (:obj:`str`): Тип.
        name (:obj:`str`): Название.
        min (:obj:`yandex_music.Value`): Минимальное значение.
        max (:obj:`yandex_music.Value`): Максимальное значение.
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.

    Args:
        type_ (:obj:`str`): Тип.
        name (:obj:`str`): Название.
        min_ (:obj:`yandex_music.Value`): Минимальное значение.
        max_ (:obj:`yandex_music.Value`): Максимальное значение.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 type_: str,
                 name: str,
                 min_: Optional['Value'],
                 max_: Optional['Value'],
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        super().handle_unknown_kwargs(self, **kwargs)

        self.type = type_
        self.name = name
        self.min = min_
        self.max = max_

        self.client = client
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
        data['min_'] = Value.de_json(data.get('min_'), client)
        data['max_'] = Value.de_json(data.get('max_'), client)

        return cls(client=client, **data)
