from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, Product, User


@model
class AutoRenewable(YandexMusicModel):
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
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.expires, self.vendor, self.vendor_help_url, self.product, self.finished)
