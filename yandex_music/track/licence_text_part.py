from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicObject
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client


@model
class LicenceTextPart(YandexMusicObject):
    """Класс, представляющий часть текста с ссылкой на лицензионное соглашение.

    Attributes:
        text (:obj:`str`): Часть текста (строка).
        url (:obj:`str`, optional): Ссылка на лицензионное соглашение.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    text: str
    url: Optional[str] = None
    client: Optional['Client'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.text,)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['LicenceTextPart']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.LicenceTextPart`: Строка лицензионного соглашения.
        """
        if not cls.is_valid_model_data(data):
            return None

        data = super(LicenceTextPart, cls).de_json(data, client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data: list, client: 'Client') -> List['LicenceTextPart']:
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.LicenceTextPart`: Строки текста с ссылкой на лицензионное соглашение.
        """
        if not cls.is_valid_model_data(data, array=True):
            return []

        return [cls.de_json(row, client) for row in data]
