from typing import List, TYPE_CHECKING, Optional

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client, Deactivation


class Operator(YandexMusicObject):
    """Класс, представляющий услугу сотового оператора.

    Attributes:
        product_id (:obj:`str`): Уникальный идентификатор продукта сервиса Яндекс.Музыка.
        phone (:obj:`str`): Мобильный номер, на который подключена услуга.
        payment_regularity (:obj:`str`): Регулярность оплаты.
        deactivation (:obj:`list` из :obj:`yandex_music.Deactivation`): Способы деактивации.
        title (:obj:`str`): Название услуги.
        suspended (:obj:`bool`): Приостановлено.
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.

    Args:
        product_id (:obj:`str`): Уникальный идентификатор продукта сервиса Яндекс.Музыка.
        phone (:obj:`str`): Мобильный номер, на который подключена услуга.
        payment_regularity (:obj:`str`): Регулярность оплаты.
        deactivation (:obj:`list` из :obj:`yandex_music.Deactivation`): Способы деактивации.
        title (:obj:`str`): Название услуги.
        suspended (:obj:`bool`): Приостановлено.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(
        self,
        product_id: str,
        phone: str,
        payment_regularity: str,
        deactivation: List['Deactivation'],
        title: str,
        suspended: bool,
        client: Optional['Client'] = None,
        **kwargs,
    ) -> None:
        self.product_id = product_id
        self.phone = phone
        self.payment_regularity = payment_regularity
        self.deactivation = deactivation
        self.title = title
        self.suspended = suspended

        self.client = client
        self._id_attrs = (self.product_id, self.phone)

        super().handle_unknown_kwargs(self, **kwargs)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Operator']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Operator`: Услуга сотового оператора.
        """
        if not data:
            return None

        from yandex_music import Deactivation

        data['deactivation'] = Deactivation.de_list(data.get('deactivation'), client)

        data = super(Operator, cls).de_json(data, client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data: dict, client: 'Client') -> List['Operator']:
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.Operator`: Услуги сотового оператора.
        """
        if not data:
            return []

        return [cls.de_json(operator, client) for operator in data]
