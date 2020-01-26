from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client


class Id(YandexMusicObject):
    """Класс, представляющий .

    Attributes:
        client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

    Args:
        client (:obj:`yandex_music.Client`, optional): Объект класса :class:`yandex_music.Client`, представляющий клиент
            Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 type_: str,
                 tag: str,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        self.type = type_
        self.tag = tag

        self.client = client
        self._id_attrs = (self.type, self.tag)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Id']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

        Returns:
            :obj:`yandex_music.Id`: Объект класса :class:`yandex_music.Id`.
        """
        if not data:
            return None

        data = super(Id, cls).de_json(data, client)

        return cls(client=client, **data)
