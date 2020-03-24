from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client


class CaseForms(YandexMusicObject):
    """Класс, представляющий склонение имени.

    Attributes:
        nominative (:obj:`str`): Именительный.
        genitive (:obj:`str`): Родительный.
        dative (:obj:`str`): Дательный.
        accusative (:obj:`str`): Винительный.
        instrumental (:obj:`str`): Творительный.
        prepositional (:obj:`str`): Предложный.
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.

    Args:
        nominative (:obj:`str`): Именительный.
        genitive (:obj:`str`): Родительный.
        dative (:obj:`str`): Дательный.
        accusative (:obj:`str`): Винительный.
        instrumental (:obj:`str`): Творительный.
        prepositional (:obj:`str`): Предложный.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 nominative: str,
                 genitive: str,
                 dative: str,
                 accusative: str,
                 instrumental: str,
                 prepositional: str,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        super().handle_unknown_kwargs(self, **kwargs)

        self.nominative = nominative
        self.genitive = genitive
        self.dative = dative
        self.accusative = accusative
        self.instrumental = instrumental
        self.prepositional = prepositional

        self.client = client
        self._id_attrs = (self.nominative, self.genitive, self.dative,
                          self.accusative, self.instrumental, self.prepositional)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['CaseForms']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.CaseForms`: TODO.
        """
        if not data:
            return None

        data = super(CaseForms, cls).de_json(data, client)

        return cls(client=client, **data)
