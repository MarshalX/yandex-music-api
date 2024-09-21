from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType, Price, Product


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

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['Settings']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Settings`: Предложение по покупке.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music import Price, Product

        cls_data['in_app_products'] = Product.de_list(data.get('in_app_products'), client)
        cls_data['native_products'] = Product.de_list(data.get('native_products'), client)
        cls_data['web_payment_month_product_price'] = Price.de_json(data.get('web_payment_month_product_price'), client)

        return cls(client=client, **cls_data)  # type: ignore
