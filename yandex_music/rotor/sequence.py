from typing import TYPE_CHECKING, Optional, List

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client, Track


class Sequence(YandexMusicObject):
    """Класс, представляющий звено последовательности.

    Note:
        Известные значения поля `type_`: `track`. Возможно есть `ad`.

    Attributes:
        type_ (:obj:`str`): Тип звена.
        track (:obj:`yandex_music.Track` | :obj:`None`): Трек.
        liked (:obj:`bool`): Связанное ли.
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.

    Args:
        type_ (:obj:`str`): Тип звена.
        track (:obj:`yandex_music.Track` | :obj:`None`): Трек.
        liked (:obj:`bool`): Связанное ли.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 type_: str,
                 track: Optional['Track'],
                 liked: bool,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        super().handle_unknown_kwargs(self, **kwargs)

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
            :obj:`yandex_music.Sequence`: Звено последовательности.
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
            :obj:`list` из :obj:`yandex_music.Sequence`: Последовательность треков.
        """
        if not data:
            return []

        sequences = list()
        for sequence in data:
            sequences.append(cls.de_json(sequence, client))

        return sequences
