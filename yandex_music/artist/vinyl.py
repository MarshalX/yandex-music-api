from typing import TYPE_CHECKING, Optional, List

from yandex_music import YandexMusicObject
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client


@model
class Vinyl(YandexMusicObject):
    """Класс, представляющий виниловую пластинку.

    Attributes:
        url (:obj:`str`): Ссылка на пластинку в магазине.
        title (:obj:`str`): Заголовок.
        year (:obj:`int`): Год выпуска.
        price (:obj:`int`): Цена.
        media (:obj:`str`): Средство распространения.
        offer_id (:obj:`int`): Уникальный идентификатор предложения.
        artist_ids (:obj:`list` из :obj:`int`): Перечень уникальный идентификаторов исполнителей.
        picture (:obj:`str`, optional): Ссылка на обложку.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    url: str
    title: str
    year: int
    price: int
    media: str
    offer_id: int
    artist_ids: List[int]
    picture: Optional[str] = None
    client: Optional['Client'] = None

    def __post_init__(self):
        self._id_attrs = (
            self.title,
            self.price,
            self.year,
            self.url,
            self.price,
            self.media,
            self.offer_id,
            self.artist_ids,
        )

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
