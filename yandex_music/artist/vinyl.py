from typing import TYPE_CHECKING, Optional, List

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client


class Vinyl(YandexMusicObject):
    """Класс, представляющий виниловую пластинку.

    Attributes:
        url (:obj:`str`): Ссылка на пластинку в магазине.
        title (:obj:`str`): Заголовок.
        year (:obj:`int`): Год выпуска.
        price (:obj:`int`): Цена.
        media (:obj:`str`): Средство распространения.
        picture (:obj:`str`): Ссылка на обложку.
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.

    Args:
        url (:obj:`str`): Ссылка на пластинку в магазине.
        title (:obj:`str`): Заголовок.
        year (:obj:`int`): Год выпуска.
        price (:obj:`int`): Цена.
        media (:obj:`str`): Средство распространения.
        picture (:obj:`str`, optional): Ссылка на обложку.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 url: str,
                 title: str,
                 year: int,
                 price: int,
                 media: str,
                 picture: Optional[str] = None,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        super().handle_unknown_kwargs(self, **kwargs)

        self.url = url
        self.picture = picture
        self.title = title
        self.year = year
        self.price = price
        self.media = media

        self.client = client
        self._id_attrs = (self.title, self.price, self.year, self.url, self.price, self.media)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Vinyl']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Vinyl`: Ваниловая пластинка.
        """
        if not data:
            return None

        data = super(Vinyl, cls).de_json(data, client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data: dict, client: 'Client') -> List['Vinyl']:
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.Vinyl`: Ваниловые пластинки.
        """
        if not data:
            return []

        vinyls = list()
        for vinyl in data:
            vinyls.append(cls.de_json(vinyl, client))

        return vinyls
