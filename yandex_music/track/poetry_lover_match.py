from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicObject
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client


@model
class PoetryLoverMatch(YandexMusicObject):
    """Класс, представляющий слова в тексте TODO.

    Note:
        Некая разметка для обучения чего-нибудь для написания романтических стихотворений.

    Attributes:
        begin (:obj:`int`): Индекс начала.
        end (:obj:`int`): Индекс конца.
        line (:obj:`int`): Индекс строки.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    begin: int
    end: int
    line: int
    client: Optional['Client'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.begin, self.end, self.line)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['PoetryLoverMatch']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.PoetryLoverMatch`: Позиция слова.
        """
        if not cls.is_valid_model_data(data):
            return None

        data = super(PoetryLoverMatch, cls).de_json(data, client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data: list, client: 'Client') -> List['PoetryLoverMatch']:
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.PoetryLoverMatch`: Список с позициями слов.
        """
        if not cls.is_valid_model_data(data, array=True):
            return []

        return [cls.de_json(match, client) for match in data]
