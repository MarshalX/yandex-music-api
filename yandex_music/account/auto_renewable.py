from typing import TYPE_CHECKING, Optional, List

from yandex_music import YandexMusicObject
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client, Product, User


@model
class AutoRenewable(YandexMusicObject):
    """Класс, представляющий информацию об автопродлении подписки.

    Attributes:
        expires (:obj:`str`): Дата истечения подписки.
        vendor (:obj:`str`): Продавец.
        vendor_help_url (:obj:`str`): Ссылка на страницу помощи продавца.
        product_id (:obj:`str`): Уникальный идентификатор продукта.
        finished (:obj:`bool`): Завершенность автопродления.
        master_info (:obj:`yandex_music.User`, optional): Главный в семейной подписке.
        product (:obj:`yandex_music.Product`, optional): Продукт.
        order_id (:obj:`int`): Уникальный идентификатор заказа.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    expires: str
    vendor: str
    vendor_help_url: str
    product: Optional['Product']
    finished: bool
    master_info: Optional['User'] = None
    product_id: Optional[str] = None
    order_id: Optional[int] = None
    client: Optional['Client'] = None

    def __post_init__(self):
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
        from yandex_music import Product, User

        data['product'] = Product.de_json(data.get('product'), client)
        data['master_info'] = User.de_json(data.get('master_info'), client)

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

        return [cls.de_json(auto_renewable, client) for auto_renewable in data]
