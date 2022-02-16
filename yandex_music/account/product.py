from typing import TYPE_CHECKING, Optional, List

from yandex_music import YandexMusicObject
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client, Price


@model
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
        plus (:obj:`bool`): Даёт ли подписку "Плюс".
        cheapest (:obj:`bool`, optional): Самый дешёвый (лучшее предложение).
        title (:obj:`str`, optional): Заголовок продукта.
        family_sub (:obj:`bool`, optional): Семейная ли подписка.
        fb_image (:obj:`str`, optional): Картинка для превью на facebook.
        fb_name (:obj:`str`, optional): Заголовок превью на facebook.
        family (:obj:`bool`, optional): Доступно ли для семьи.
        features (:obj:`list` из :obj:`str`, optional): Список предоставляемых возможностей.
        description (:obj:`str`, optional): Описание.
        available (:obj:`bool`, optional): Доступна ли покупка.
        trial_available (:obj:`bool`, optional): Доступен ли пробный период.
        trial_period_duration (:obj:`str`, optional): Длительность пробного периода.
        intro_period_duration (:obj:`str`, optional): Длительность вступительного периода TODO.
        intro_price (:obj:`yandex_music.Price`, optional): Цена вступительного периода.
        start_period_duration (:obj:`str`, optional): Длительность первого срока (за меньшую цену).
        start_price (:obj:`yandex_music.Price`, optional): Цена за первый срок.
        licence_text_parts (:obj:`list` из :obj:`yandex_music.LicenceTextPart`, optional):
            Длительность пробного периода.
        vendor_trial_available (:obj:`bool`, optional): Доступен испытательный срок продавца TODO.
        button_text (:obj:`str`, optional): Текст кнопки.
        button_additional_text (:obj:`str`, optional): Дополнительный текст кнопки.
        payment_method_types (:obj:`list` из :obj:`str`, optional): Способы оплаты.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    product_id: str
    type: str
    common_period_duration: str
    duration: int
    trial_duration: int
    price: Optional['Price']
    feature: str
    debug: bool
    plus: bool
    cheapest: Optional[bool] = None
    title: Optional[str] = None
    family_sub: Optional[bool] = None
    fb_image: Optional[str] = None
    fb_name: Optional[str] = None
    family: Optional[bool] = None
    features: List[str] = None
    description: Optional[str] = None
    available: Optional[bool] = None
    trial_available: Optional[bool] = None
    trial_period_duration: Optional[str] = None
    intro_period_duration: Optional[str] = None
    intro_price: Optional['Price'] = None
    start_period_duration: Optional[str] = None
    start_price: Optional['Price'] = None
    licence_text_parts: List['Price'] = None
    vendor_trial_available: Optional[bool] = None
    button_text: Optional[str] = None
    button_additional_text: Optional[str] = None
    payment_method_types: List[str] = None
    client: Optional['Client'] = None

    def __post_init__(self):
        self._id_attrs = (
            self.product_id,
            self.type,
            self.common_period_duration,
            self.duration,
            self.trial_duration,
            self.product_id,
            self.feature,
            self.debug,
        )

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Product']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Product`: Продаваемый продукт.
        """
        if not data:
            return None

        data = super(Product, cls).de_json(data, client)
        from yandex_music import Price, LicenceTextPart

        data['price'] = Price.de_json(data.get('price'), client)
        data['intro_price'] = Price.de_json(data.get('intro_price'), client)
        data['start_price'] = Price.de_json(data.get('start_price'), client)
        data['licence_text_parts'] = LicenceTextPart.de_list(data.get('licence_text_parts'), client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data: dict, client: 'Client') -> List['Product']:
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.Product`: Продаваемые продукты.
        """
        if not data:
            return []

        return [cls.de_json(product, client) for product in data]
