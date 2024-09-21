from typing import TYPE_CHECKING, Optional

from yandex_music import DiscreteScale, Enum, JSONType, YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType

de_json = {'enum': Enum.de_json, 'discrete-scale': DiscreteScale.de_json}


@model
class Restrictions(YandexMusicModel):
    """Класс, представляющий ограничения для настроек станции.

    Attributes:
        language (:obj:`yandex_music.Enum`): Перечисление значений для языков.
        diversity (:obj:`yandex_music.Enum`): Перечисление значений для разнообразия (треков).
        mood (:obj:`yandex_music.DiscreteScale`, optional): Ограничение для значений настроения.
        energy (:obj:`yandex_music.DiscreteScale`, optional): Ограничение для значений энергичности.
        mood_energy (:obj:`yandex_music.Enum`, optional): Значения для настроения.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    language: Optional['Enum']
    diversity: Optional['Enum']
    mood: Optional['DiscreteScale'] = None
    energy: Optional['DiscreteScale'] = None
    mood_energy: Optional['Enum'] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.language, self.diversity)

    @classmethod
    def de_json(cls, data: JSONType, client: 'ClientType') -> Optional['Restrictions']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Restrictions`: Ограничения для настроек станции.
        """
        if not cls.is_dict_model_data(data):
            return None

        data = cls.cleanup_data(data, client)

        for key, value in data.items():
            data[key] = de_json.get(value.get('type'))(value, client)

        return cls(client=client, **data)
