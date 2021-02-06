from typing import TYPE_CHECKING, Optional, List

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client


class LicenceTextPart(YandexMusicObject):
    """Класс, представляющий часть текста с ссылкой на лицензионное соглашение.

    Attributes:
        text (:obj:`str`): Часть текста (строка).
        url (:obj:`str`): Ссылка на лицензионное соглашение.
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.

    Args:
        text (:obj:`str`): Часть текста (строка).
        url (:obj:`str`, optional): Ссылка на лицензионное соглашение.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self, text: str, url: Optional[str] = None, client: Optional['Client'] = None, **kwargs) -> None:
        self.text = text

        self.url = url

        self.client = client
        self._id_attrs = (self.text,)

        super().handle_unknown_kwargs(self, **kwargs)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['PassportPhone']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.LicenceTextPart`: Строка лицензионного соглашения.
        """
        if not data:
            return None

        data = super(LicenceTextPart, cls).de_json(data, client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data: dict, client: 'Client') -> List['LicenceTextPart']:
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.LicenceTextPart`: Строки текста с ссылкой на лицензионное соглашение.
        """
        if not data:
            return []

        return [cls.de_json(row, client) for row in data]
