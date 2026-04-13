from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType
    from yandex_music.concert.concert_cashback import ConcertCashback
    from yandex_music.concert.concert_event_info import ConcertEventInfo
    from yandex_music.concert.concert_min_price import ConcertMinPrice


@model
class Concert(YandexMusicModel):
    """Класс, представляющий концерт.

    Note:
        Известные значения поля event_info.type: concert, festival.

    Attributes:
        id (:obj:`str`, optional): UUID концерта.
        images (:obj:`list` из :obj:`str`, optional): Список URL изображений.
        image_url (:obj:`str`, optional): URL основного изображения.
        concert_title (:obj:`str`, optional): Название концерта/фестиваля.
        afisha_url (:obj:`str`, optional): Ссылка на страницу Афиши.
        city (:obj:`str`, optional): Город.
        place (:obj:`str`, optional): Площадка.
        address (:obj:`str`, optional): Адрес.
        datetime (:obj:`str`, optional): Дата и время (ISO 8601).
        content_rating (:obj:`str`, optional): Возрастной рейтинг, например "16+".
        min_price (:obj:`yandex_music.ConcertMinPrice`, optional): Минимальная цена билета.
        cashback (:obj:`yandex_music.ConcertCashback`, optional): Информация о кешбэке.
        event_info (:obj:`yandex_music.ConcertEventInfo`, optional): Информация о типе события.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    id: Optional[str] = None
    images: Optional[List[str]] = None
    image_url: Optional[str] = None
    concert_title: Optional[str] = None
    afisha_url: Optional[str] = None
    city: Optional[str] = None
    place: Optional[str] = None
    address: Optional[str] = None
    datetime: Optional[str] = None
    content_rating: Optional[str] = None
    min_price: Optional['ConcertMinPrice'] = None
    cashback: Optional['ConcertCashback'] = None
    event_info: Optional['ConcertEventInfo'] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.id,)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['Concert']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Concert`: Концерт.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music.concert.concert_cashback import ConcertCashback
        from yandex_music.concert.concert_event_info import ConcertEventInfo
        from yandex_music.concert.concert_min_price import ConcertMinPrice

        cls_data['min_price'] = ConcertMinPrice.de_json(cls_data.get('min_price'), client)
        cls_data['cashback'] = ConcertCashback.de_json(cls_data.get('cashback'), client)
        cls_data['event_info'] = ConcertEventInfo.de_json(cls_data.get('event_info'), client)

        return cls(client=client, **cls_data)  # type: ignore
