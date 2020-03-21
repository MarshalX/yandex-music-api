from typing import TYPE_CHECKING, Optional, List

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client, Track


class Sequence(YandexMusicObject):
    """Класс, представляющий .

    Attributes:
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.

    Args:
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 type_: str,
                 track: Optional['Track'],
                 liked: bool,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        self.type = type_
        self.track = track
        self.liked = liked

        self.client = client
        self._id_attrs = (self.type, self.track, self.liked)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Sequence']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Sequence`: TODO.
        """
        if not data:
            return None

        data = super(Sequence, cls).de_json(data, client)
        from yandex_music import Track
        data['track'] = Track.de_json(data.get('track'), client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data: dict, client: 'Client') -> List['Sequence']:
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.Sequence`: TODO.
        """
        if not data:
            return []

        sequences = list()
        for sequence in data:
            sequences.append(cls.de_json(sequence, client))

        return sequences
