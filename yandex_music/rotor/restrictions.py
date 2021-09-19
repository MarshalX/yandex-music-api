from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicObject, Enum, DiscreteScale
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client

de_json = {'enum': Enum.de_json, 'discrete-scale': DiscreteScale.de_json}


@model
class Restrictions(YandexMusicObject):
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
    client: Optional['Client'] = None

    def __post_init__(self):
        self._id_attrs = (self.language, self.diversity)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Restrictions']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Restrictions`: Ограничения для настроек станции.
        """
        if not data:
            return None

        data = super(Restrictions, cls).de_json(data, client)

        for key, value in data.items():
            data[key] = de_json.get(value.get('type'))(value, client)

        return cls(client=client, **data)
