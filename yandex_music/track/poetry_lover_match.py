from typing import TYPE_CHECKING, Optional, List

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client


class PoetryLoverMatch(YandexMusicObject):
    """Класс, представляющий слова в тексте TODO.

    Note:
        Некая разметка для обучения чего-нибудь для написания романтических стихотворений.

    Attributes:
        begin (:obj:`int`): Индекс начала.
        end (:obj:`int`): Индекс конца.
        line (:obj:`int`): Индекс строки.
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.

    Args:
        begin (:obj:`int`): Индекс начала.
        end (:obj:`int`): Индекс конца.
        line (:obj:`int`): Индекс строки.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self, begin: int, end: int, line: int, client: Optional['Client'] = None, **kwargs) -> None:
        self.begin = begin
        self.end = end
        self.line = line

        self.client = client
        self._id_attrs = (self.begin, self.end, self.line)

        super().handle_unknown_kwargs(self, **kwargs)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['PoetryLoverMatch']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.PoetryLoverMatch`: Позиция слова.
        """
        if not data:
            return None

        data = super(PoetryLoverMatch, cls).de_json(data, client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data: dict, client: 'Client') -> List['PoetryLoverMatch']:
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.PoetryLoverMatch`: Список с позициями слов.
        """
        if not data:
            return []

        return [cls.de_json(match, client) for match in data]
