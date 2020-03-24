from typing import TYPE_CHECKING, Optional, List

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client, Value


class Enum(YandexMusicObject):
    """Класс, представляющий перечисления.

    Attributes:
        type (:obj:`str`): Тип перечисления.
        name (:obj:`str`): Название перечисления.
        possible_values (:obj:`list` из :obj:`yandex_Music.Value`): Доступные значения.
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.

    Args:
        type_ (:obj:`str`): Тип перечисления.
        name (:obj:`str`): Название перечисления.
        possible_values (:obj:`list` из :obj:`yandex_Music.Value`): Доступные значения.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 type_: str,
                 name: str,
                 possible_values: List['Value'],
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        super().handle_unknown_kwargs(self, **kwargs)

        self.type = type_
        self.name = name
        self.possible_values = possible_values

        self.client = client
        self._id_attrs = (self.type, self.name, self.possible_values)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Enum']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Enum`: Перечисление.
        """
        if not data:
            return None

        data = super(Enum, cls).de_json(data, client)
        from yandex_music import Value
        data['possible_values'] = Value.de_list(data.get('possible_values'), client)

        return cls(client=client, **data)
