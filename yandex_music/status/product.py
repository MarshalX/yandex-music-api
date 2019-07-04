from yandex_music import YandexMusicObject, Price


class Product(YandexMusicObject):
    """Класс представляющий продаваемый продукт.

    Attributes:
        product_id (:obj:`str`): Уникальный идентификатор.
        type (:obj:`str`): Тип продаваемого.
        common_period_duration (:obj:`str`): Длительность общего периода.
        duration (:obj:`int`): Длительность.
        trial_duration (:obj:`int`): Длительность испытательного срока.
        price (:obj:`yandex_music.Price`): Объект класса :class:`yandex_music.Price` представляющий цену.
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
        client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
            Music.

    Args:
        product_id (:obj:`str`): Уникальный идентификатор.
        type (:obj:`str`): Тип продаваемого.
        common_period_duration (:obj:`str`): Длительность общего периода.
        duration (:obj:`int`): Длительность.
        trial_duration (:obj:`int`): Длительность испытательного срока.
        price (:obj:`yandex_music.Price`): Объект класса :class:`yandex_music.Price` представляющий цену.
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
        client (:obj:`yandex_music.Client`, optional): Объект класса :class:`yandex_music.Client` представляющий клиент
            Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 product_id,
                 type,
                 common_period_duration,
                 duration,
                 trial_duration,
                 price,
                 feature,
                 debug,
                 features=None,
                 description=None,
                 available=None,
                 trial_available=None,
                 vendor_trial_available=None,
                 button_text=None,
                 button_additional_text=None,
                 payment_method_types=None,
                 client=None,
                 **kwargs):
        self.product_id = product_id
        self.type = type
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
        self._id_attrs = (self.product_id,)

    @classmethod
    def de_json(cls, data, client):
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
                Music.

        Returns:
            :obj:`yandex_music.Product`: Объект класса :class:`yandex_music.Product`.
        """
        if not data:
            return None

        data = super(Product, cls).de_json(data, client)
        data['price'] = Price.de_json(data.get('price'), client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data, client):
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
                Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.Product`: Список объектов класса :class:`yandex_music.Product`.
        """
        if not data:
            return []

        products = list()
        for product in data:
            products.append(cls.de_json(product, client))

        return products
