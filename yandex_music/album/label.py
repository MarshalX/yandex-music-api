from typing import TYPE_CHECKING, Optional, List, Union

from yandex_music import YandexMusicObject
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client


@model
class Label(YandexMusicObject):
    """Класс, представляющий лейбл альбома.

    Attributes:
        id (:obj:`int`): Идентификатор альбома.
        name (:obj:`str`): Название альбома.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    id: int
    name: str
    client: Optional['Client'] = None

    def __post_init__(self):
        self._id_attrs = (self.id, self.name)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Label']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        Returns:
            :obj:`yandex_music.Label`: Лейбл.
        """
        if not data:
            return None

        data = super(Label, cls).de_json(data, client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data: dict, client: 'Client') -> List[Union['Label', str]]:
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Note:
            Лейблы строками возвращаются, как минимум, в результатах поиска. В остальных местах это объекты.

        Returns:
            :obj:`list` из :obj:`yandex_music.Label` или :obj:`str`: Лейблы.
        """
        if not data:
            return []

        labels = list()
        for label in data:
            if isinstance(label, dict):
                labels.append(cls.de_json(label, client))
            else:
                labels.append(label)

        return labels
