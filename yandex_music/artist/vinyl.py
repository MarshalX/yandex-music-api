from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType


@model
class Vinyl(YandexMusicModel):
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
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
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
