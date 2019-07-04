from yandex_music import YandexMusicObject


class Settings(YandexMusicObject):
    """Класс представляющий предложения по покупке.

    Attributes:
        in_app_products (:obj:`list` из :obj:`yandex_music.Product`): Список объектов класса
            :class:`yandex_music.Product` представляющий продаваемые продукты внутри приложения.
        native_products (:obj:`list`) из :obj:`yandex_music.Product`: Список объектов класса
            :class:`yandex_music.Product` представляющий продаваемые продукты всплывающими окнами.
        web_payment_url (:obj:`str`): Ссылка для осуществления платежа.
        web_payment_month_product_price (:obj:`yandex_music.Price`): Объект класса :class:`yandex_music.Price`
            представляющий цену продукта за месяц.
        promo_codes_enabled (:obj:`bool`): Доступно ли использование промо-кодов.
        client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
            Music.

    Args:
        in_app_products (:obj:`list` из :obj:`yandex_music.Product`): Список объектов класса
            :class:`yandex_music.Product` представляющий продаваемые продукты внутри приложения.
        native_products (:obj:`list`) из :obj:`yandex_music.Product`: Список объектов класса
            :class:`yandex_music.Product` представляющий продаваемые продукты всплывающими окнами.
        web_payment_url (:obj:`str`): Ссылка для осуществления платежа.
        web_payment_month_product_price (:obj:`yandex_music.Price`, optional): Объект класса :class:`yandex_music.Price`
            представляющий цену продукта за месяц.
        promo_codes_enabled (:obj:`bool`): Доступно ли использование промо-кодов.
        client (:obj:`yandex_music.Client`, optional): Объект класса :class:`yandex_music.Client` представляющий клиент
            Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 in_app_products,
                 native_products,
                 web_payment_url,
                 promo_codes_enabled,
                 web_payment_month_product_price=None,
                 client=None,
                 **kwargs):
        self.in_app_products = in_app_products
        self.native_products = native_products
        self.web_payment_url = web_payment_url
        self.web_payment_month_product_price = web_payment_month_product_price
        self.promo_codes_enabled = promo_codes_enabled

        self.client = client

    @classmethod
    def de_json(cls, data, client):
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
                Music.

        Returns:
            :obj:`yandex_music.Settings`: Объект класса :class:`yandex_music.Settings`.
        """
        if not data:
            return None

        data = super(Settings, cls).de_json(data, client)
        from yandex_music import Product, Price
        data['in_app_products'] = Product.de_list(data.get('in_app_products'), client)
        data['native_products'] = Product.de_list(data.get('native_products'), client)
        data['web_payment_month_product_price'] = \
            Price.de_json(data.get('web_payment_month_product_price'), client)

        return cls(client=client, **data)
