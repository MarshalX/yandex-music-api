from typing import TYPE_CHECKING, Optional, List

if TYPE_CHECKING:
    from yandex_music import Client

from yandex_music import YandexMusicObject


class Label(YandexMusicObject):
    """Класс, представляющий лейбл альбома.

        Attributes:
            id (:obj:`int`): Идентификатор альбома.
            name (:obj:`str`): Название альбома.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
                Music.
        Args:
            id_ (:obj:`int`): Идентификатор альбома.
            name (:obj:`str`): Название альбома.
            client (:obj:`yandex_music.Client`, optional): Объект класса :class:`yandex_music.Client` представляющий
                клиент Yandex Music.
            **kwargs: Произвольные ключевые аргументы полученные от API.
        """
    def __init__(self,
                 id_: int,
                 name: str,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        self.id = id_
        self.name = name

        self.client = client
        self._id_attrs = (self.id, self.name)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Label']:
        """Десериализация объекта.
        
             Args:
                 data (:obj:`dict`): Поля и значения десериализуемого объекта.
                 client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент
                    Yandex Music.
             Returns:
                 :obj:`yandex_music.Label`: Объект класса :class:`yandex_music.Label`.
        """
        if not data:
            return None

        data = super(Label, cls).de_json(data, client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data: dict, client: 'Client') -> List['Label']:
        """Десериализация списка объектов.
        
            Args:
                data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
                client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент
                    Yandex Music.
            Returns:
                :obj:`list` из :obj:`yandex_music.Label`: Список объектов класса :class:`yandex_music.Label`.
        """
        if not data:
            return []

        labels = list()
        for label in data:
            labels.append(cls.de_json(label, client))

        return labels
