from typing import List, TYPE_CHECKING, Optional

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client


class Deactivation(YandexMusicObject):
    """Класс, представляющий способы деактивации мобильной услуги.

    Note:
        Известные значения поля `method`: `ussd`.

    Attributes:
        method (:obj:`str`): Метод отключения.
        instructions (:obj:`str`): Инструкция.
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.

    Args:
        method (:obj:`str`): Метод отключения.
        instructions (:obj:`str`, optional): Инструкция.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(
        self, method: str, instructions: Optional[str] = None, client: Optional['Client'] = None, **kwargs
    ) -> None:
        self.method = method
        self.instructions = instructions

        self.client = client
        self._id_attrs = (self.method, self.instructions)

        super().handle_unknown_kwargs(self, **kwargs)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Deactivation']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Deactivation`: Способ отключения услуги.
        """
        if not data:
            return None

        data = super(Deactivation, cls).de_json(data, client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data: dict, client: 'Client') -> List['Deactivation']:
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.Deactivation`: Способы отключения услуги.
        """
        if not data:
            return []

        return [cls.de_json(deactivation, client) for deactivation in data]
