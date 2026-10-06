from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, Price, Product


@model
class Settings(YandexMusicModel):
    """Класс, представляющий предложения по покупке.

    Attributes:
        in_app_products (:obj:`list` из :obj:`yandex_music.Product`): Продаваемые продукты внутри приложения.
        native_products (:obj:`list`) из :obj:`yandex_music.Product`: Продаваемые продукты всплывающими окнами.
        web_payment_url (:obj:`str`): Ссылка для осуществления платежа.
        web_payment_month_product_price (:obj:`yandex_music.Price`, optional): Цена продукта за месяц.
        promo_codes_enabled (:obj:`bool`): Доступно ли использование промо-кодов.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    in_app_products: List['Product']
    native_products: List['Product']
    web_payment_url: str
    promo_codes_enabled: bool
    web_payment_month_product_price: Optional['Price'] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.in_app_products, self.native_products, self.web_payment_url, self.promo_codes_enabled)
