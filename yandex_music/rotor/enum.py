from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType, Value


@model
class Enum(YandexMusicModel):
    """Класс, представляющий перечисления.

    Attributes:
        type (:obj:`str`): Тип перечисления.
        name (:obj:`str`): Название перечисления.
        possible_values (:obj:`list` из :obj:`yandex_music.Value`): Доступные значения.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    type: str
    name: str
    possible_values: List['Value']
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.type, self.name, self.possible_values)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['Enum']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Enum`: Перечисление.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music import Value

        cls_data['possible_values'] = Value.de_list(data.get('possible_values'), client)

        return cls(client=client, **cls_data)  # type: ignore
