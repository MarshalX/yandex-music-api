from typing import TYPE_CHECKING, Optional, List

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client, Product


class AutoRenewable(YandexMusicObject):
    """Класс, представляющий информацию об автопродлении подписки.

    Attributes:
        expires (:obj:`str`): Дата истечения подписки.
        vendor (:obj:`str`): Продавец.
        vendor_help_url (:obj:`str`): Ссылка на страницу помощи продавца.
        product_id (:obj:`str`): Уникальный идентификатор продукта.
        product (:obj:`yandex_music.Product`): Продукт.
        order_id (:obj:`int`): Уникальный идентификатор заказа.
        finished (:obj:`bool`): Завершенность автопродления.
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.

    Args:
        expires (:obj:`str`): Дата истечения подписки.
        vendor (:obj:`str`): Продавец.
        vendor_help_url (:obj:`str`): Ссылка на страницу помощи продавца.
        product_id (:obj:`str`): Уникальный идентификатор продукта.
        finished (:obj:`bool`): Завершенность автопродления.
        product (:obj:`yandex_music.Product`, optional): Продукт.
        order_id (:obj:`int`): Уникальный идентификатор заказа.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 expires: str,
                 vendor: str,
                 vendor_help_url: str,
                 product: Optional['Product'],
                 finished: bool,
                 product_id: Optional[str] = None,
                 order_id: Optional[int] = None,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        super().handle_unknown_kwargs(self, **kwargs)

        self.expires = expires
        self.vendor = vendor
        self.vendor_help_url = vendor_help_url
        self.product = product
        self.finished = finished

        self.product_id = product_id
        self.order_id = order_id

        self.client = client
        self._id_attrs = (self.expires, self.vendor, self.vendor_help_url, self.product, self.finished)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['AutoRenewable']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.AutoRenewable`: Информация об автопродлении подписки.
        """
        if not data:
            return None

        data = super(AutoRenewable, cls).de_json(data, client)
        from yandex_music import Product
        data['product'] = Product.de_json(data.get('product'), client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data: dict, client: 'Client') -> List['AutoRenewable']:
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.AutoRenewable`: Информация об автопродлении подписки.
        """
        if not data:
            return []

        auto_renewables = list()
        for auto_renewable in data:
            auto_renewables.append(cls.de_json(auto_renewable, client))

        return auto_renewables
