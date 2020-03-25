from typing import TYPE_CHECKING, Optional, List

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client


class Label(YandexMusicObject):
    """Класс, представляющий лейбл альбома.

    Attributes:
        id (:obj:`int`): Идентификатор альбома.
        name (:obj:`str`): Название альбома.
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.
    Args:
        id_ (:obj:`int`): Идентификатор альбома.
        name (:obj:`str`): Название альбома.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 id_: int,
                 name: str,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        super().handle_unknown_kwargs(self, **kwargs)

        self.id = id_
        self.name = name

        self.client = client
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
    def de_list(cls, data: dict, client: 'Client') -> List['Label']:
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.Label`: Лейблы.
        """
        if not data:
            return []

        labels = list()
        for label in data:
            labels.append(cls.de_json(label, client))

        return labels
