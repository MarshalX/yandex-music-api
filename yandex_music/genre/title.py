from typing import TYPE_CHECKING, Optional, Dict

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client


class Title(YandexMusicObject):
    """Класс, представляющий заголовок жанра.

    Attributes:
        title (:obj:`str`): Заголовок.
        full_title (:obj:`str`): Полный заголовок.
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.

    Args:
        title (:obj:`str`): Заголовок.
        full_title (:obj:`str`, optional): Полный заголовок.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 title: str,
                 full_title: Optional[str] = None,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        self.title = title
        self.full_title = full_title

        self.client = client
        self._id_attrs = (self.title, self.full_title)

        super().handle_unknown_kwargs(self, **kwargs)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Title']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Title`: Заголовок жанра.
        """
        if not data:
            return None

        data = super(Title, cls).de_json(data, client)

        return cls(client=client, **data)

    @classmethod
    def de_dict(cls, data, client) -> Dict[str, Optional['Title']]:
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.Title`: Заголовки жанров.
        """
        if not data:
            return {}

        titles = dict()
        for lang, title in data.items():
            titles.update({lang: cls.de_json(title, client)})

        return titles
