from typing import TYPE_CHECKING, Optional, List

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client


class Link(YandexMusicObject):
    """Класс, представляющий ссылку на официальную страницу исполнителя.

    Note:
        Известные типы страниц: `official` - официальный сайт и `social` - социальная сеть.

    Attributes:
        title (:obj:`str`): Название страницы.
        href (:obj:`str`): URL страницы.
        type_ (:obj:`str`): Тип страницы.
        social_network (:obj:`str`): Название социальной сети.
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.

    Args:
        title (:obj:`str`): Название страницы.
        href (:obj:`str`): URL страницы.
        type_ (:obj:`str`): Тип страницы.
        social_network (:obj:`str`, optional): Название социальной сети.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    def __init__(self,
                 title: str,
                 href: str,
                 type_: str,
                 social_network: Optional[str] = None,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        super().handle_unknown_kwargs(self, **kwargs)

        self.title = title
        self.href = href
        self.type = type_

        self.social_network = social_network

        self.client = client
        self._id_attrs = (self.title, self.href, self.type)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Link']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Link`: Ссылка на официальную страницу исполнителя.
        """
        if not data:
            return None

        data = super(Link, cls).de_json(data, client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data: dict, client: 'Client') -> List['Link']:
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.Link`: Ссылки на официальные страницы исполнителя.
        """
        if not data:
            return []

        links = list()
        for link in data:
            links.append(cls.de_json(link, client))

        return links
