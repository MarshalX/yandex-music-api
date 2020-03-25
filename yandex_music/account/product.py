from typing import TYPE_CHECKING, Optional, List

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client, Price


class Product(YandexMusicObject):
    """Класс, представляющий продаваемый продукт.

    Attributes:
        product_id (:obj:`str`): Уникальный идентификатор.
        type (:obj:`str`): Тип продаваемого.
        common_period_duration (:obj:`str`): Длительность общего периода.
        duration (:obj:`int`): Длительность.
        trial_duration (:obj:`int`): Длительность испытательного срока.
        price (:obj:`yandex_music.Price`): Цена.
        feature (:obj:`str`): Предоставляемая возможность.
        debug (:obj:`bool`): Отладочный продукт.
        features (:obj:`list` из :obj:`str`): Список предоставляемых возможностей.
        description (:obj:`str`): Описание.
        available (:obj:`bool`): Доступна ли покупка.
        trial_available (:obj:`bool`): Доступен ли испытательный срок.
        vendor_trial_available (:obj:`bool`): Доступен испытательный срок продавца TODO.
        button_text (:obj:`str`): Текст кнопки.
        button_additional_text (:obj:`str`): Дополнительный текст кнопки.
        payment_method_types (:obj:`list` из :obj:`str`): Способы оплаты.
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.

    Args:
        product_id (:obj:`str`): Уникальный идентификатор.
        type_ (:obj:`str`): Тип продаваемого.
        common_period_duration (:obj:`str`): Длительность общего периода.
        duration (:obj:`int`): Длительность.
        trial_duration (:obj:`int`): Длительность испытательного срока.
        price (:obj:`yandex_music.Price`): Цена.
        feature (:obj:`str`): Предоставляемая возможность.
        debug (:obj:`bool`): Отладочный продукт.
        features (:obj:`list` из :obj:`str`, optional): Список предоставляемых возможностей.
        description (:obj:`str`, optional): Описание.
        available (:obj:`bool`, optional): Доступна ли покупка.
        trial_available (:obj:`bool`, optional): Доступен ли испытательный срок.
        vendor_trial_available (:obj:`bool`, optional): Доступен испытательный срок продавца TODO.
        button_text (:obj:`str`, optional): Текст кнопки.
        button_additional_text (:obj:`str`, optional): Дополнительный текст кнопки.
        payment_method_types (:obj:`list` из :obj:`str`, optional): Способы оплаты.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 product_id: str,
                 type_: str,
                 common_period_duration: str,
                 duration: int,
                 trial_duration: int,
                 price: Optional['Price'],
                 feature: str,
                 debug: bool,
                 features: List[str] = None,
                 description: Optional[str] = None,
                 available: Optional[bool] = None,
                 trial_available: Optional[bool] = None,
                 vendor_trial_available: Optional[bool] = None,
                 button_text: Optional[str] = None,
                 button_additional_text: Optional[str] = None,
                 payment_method_types: List[str] = None,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        super().handle_unknown_kwargs(self, **kwargs)

        self.product_id = product_id
        self.type = type_
        self.common_period_duration = common_period_duration
        self.duration = duration
        self.trial_duration = trial_duration
        self.price = price
        self.feature = feature
        self.debug = debug

        self.features = features
        self.description = description
        self.available = available
        self.trial_available = trial_available
        self.vendor_trial_available = vendor_trial_available
        self.button_text = button_text
        self.button_additional_text = button_additional_text
        self.payment_method_types = payment_method_types

        self.client = client
        self._id_attrs = (self.product_id, self.type, self.common_period_duration, self.duration,
                          self.trial_duration, self.product_id, self.feature, self.debug)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Product']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Product`: Продоваемый продукт.
        """
        if not data:
            return None

        data = super(Product, cls).de_json(data, client)
        from yandex_music import Price
        data['price'] = Price.de_json(data.get('price'), client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data: dict, client: 'Client') -> List['Product']:
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.Product`: Продоваемые продукты.
        """
        if not data:
            return []

        products = list()
        for product in data:
            products.append(cls.de_json(product, client))

        return products
