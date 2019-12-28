from typing import TYPE_CHECKING, Optional, List

if TYPE_CHECKING:
    from yandex_music import Client

from yandex_music import YandexMusicObject


class Permissions(YandexMusicObject):
    """Класс предоставляющий информацию о правах пользователя, их изначальных значениях и даты окончания.

    Attributes:
        until (:obj:`str`): Дата окончания прав.
        values (:obj:`list` из :obj:`str`): Список прав.
        default (:obj:`list` из :obj:`str`): Список изначальных прав.
        client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент
            Yandex Music.

    Args:
        until (:obj:`str`): Дата окончания прав.
        values (:obj:`list` из :obj:`str`): Список прав.
        default (:obj:`list` из :obj:`str`): Список изначальных прав.
        client (:obj:`yandex_music.Client`, optional): Объект класса :class:`yandex_music.Client` представляющий клиент
            Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 until: str,
                 values: List[str],
                 default: List[str],
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        self.until = until
        self.values = values
        self.default = default

        self.client = client
        self._id_attrs = (self.until, self.values, self.default)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Permissions']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
                Music.

        Returns:
            :obj:`yandex_music.Permissions`: Объект класса :class:`yandex_music.Permissions`.
        """
        if not data:
            return None

        data = super(Permissions, cls).de_json(data, client)

        return cls(client=client, **data)
