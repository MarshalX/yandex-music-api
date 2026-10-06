from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, Deactivation


@model
class Operator(YandexMusicModel):
    """Класс, представляющий услугу сотового оператора.

    Attributes:
        product_id (:obj:`str`): Уникальный идентификатор продукта сервиса Яндекс.Музыка.
        phone (:obj:`str`): Мобильный номер, на который подключена услуга.
        payment_regularity (:obj:`str`): Регулярность оплаты.
        deactivation (:obj:`list` из :obj:`yandex_music.Deactivation`): Способы деактивации.
        title (:obj:`str`): Название услуги.
        suspended (:obj:`bool`): Приостановлено.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    product_id: str
    phone: str
    payment_regularity: str
    deactivation: List['Deactivation']
    title: str
    suspended: bool
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.product_id, self.phone)
