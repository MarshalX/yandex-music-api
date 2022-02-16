from typing import TYPE_CHECKING, Optional, List

from yandex_music import YandexMusicObject
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client, Product, Price


@model
class Settings(YandexMusicObject):
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
    client: Optional['Client'] = None

    def __post_init__(self):
        self._id_attrs = (self.in_app_products, self.native_products, self.web_payment_url, self.promo_codes_enabled)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Settings']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Settings`: Предложение по покупке.
        """
        if not data:
            return None

        data = super(Settings, cls).de_json(data, client)
        from yandex_music import Product, Price

        data['in_app_products'] = Product.de_list(data.get('in_app_products'), client)
        data['native_products'] = Product.de_list(data.get('native_products'), client)
        data['web_payment_month_product_price'] = Price.de_json(data.get('web_payment_month_product_price'), client)

        return cls(client=client, **data)
