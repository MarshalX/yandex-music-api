from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from yandex_music import Client, Account, Permissions, Subscription, Plus

from yandex_music import YandexMusicObject


class Status(YandexMusicObject):
    """Класс представляющий подробную информацию об аккаунте пользователя.

    Attributes:
        account (:obj:`yandex_music.Account`): Объект класса :class:`yandex_music.Account` предоставляющий основную
            информацию об аккаунте.
        permissions (:obj:`yandex_music.Permissions`): Объект класса :class:`yandex_music.Permissions` предоставляющий
            информацию о правах пользователя.
        subscription (:obj:`yandex_music.Subscription`): Объект класса :class:`yandex_music.Subscription` предоставляющий
            информацию о подписках
        cache_limit (:obj:`int`): Максимальное количество загруженных треков.
        subeditor (:obj:`bool`): Наличие статуса модератора проверки корректности информации.
        subeditor_level (:obj:`int`): Уровень статуса модератора.
        plus (:obj:`yandex_music.Plus`): Объект класса :class:`yandex_music.Plus` предоставляющий информацию о Plus
            подписке.
        default_email (:obj:`str`): Основной e-mail адрес аккаунта.
        skips_per_hour (:obj:`int`): Количество переключение треков на радио в час.
        station_exists (:obj:`bool`): Наличие станции TODO.
        premium_region (:obj:`int`): Регион TODO.
        client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
            Music.

    Args:
        account (:obj:`yandex_music.Account`): Объект класса :class:`yandex_music.Account` предоставляющий основную
            информацию об аккаунте.
        permissions (:obj:`yandex_music.Permissions`): Объект класса :class:`yandex_music.Permissions` предоставляющий
            информацию о правах пользователя.
        subscription (:obj:`yandex_music.Subscription`): Объект класса :class:`yandex_music.Subscription` предоставляющий
            информацию о подписках
        cache_limit (:obj:`int`, optional): Максимальное количество загруженных треков.
        subeditor (:obj:`bool`, optional): Наличие статуса модератора проверки корректности информации.
        subeditor_level (:obj:`int`, optional): Уровень статуса модератора.
        plus (:obj:`yandex_music.Plus`, optional): Объект класса :class:`yandex_music.Plus` предоставляющий информацию о
            Plus подписке.
        default_email (:obj:`str`, optional): Основной e-mail адрес аккаунта.
        skips_per_hour (:obj:`int`, optional): Количество переключение треков на радио в час.
        station_exists (:obj:`bool`, optional): Наличие станции TODO.
        premium_region (:obj:`int`, optional): Регион TODO.
        client (:obj:`yandex_music.Client`, optional): Объект класса :class:`yandex_music.Client` представляющий клиент
            Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 account: Optional['Account'],
                 permissions: Optional['Permissions'],
                 subscription: Optional['Subscription'] = None,
                 cache_limit: Optional[int] = None,
                 subeditor: Optional[bool] = None,
                 subeditor_level: Optional[int] = None,
                 plus: Optional['Plus'] = None,
                 default_email: Optional[str] = None,
                 skips_per_hour: Optional[int] = None,
                 station_exists: Optional[bool] = None,
                 premium_region: Optional[int] = None,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        self.account = account
        self.permissions = permissions

        self.subscription = subscription
        self.cache_limit = cache_limit
        self.subeditor = subeditor
        self.subeditor_level = subeditor_level
        self.plus = plus
        self.default_email = default_email
        self.skips_per_hour = skips_per_hour
        self.station_exists = station_exists
        self.premium_region = premium_region

        self.client = client
        self._id_attrs = (self.account, self.permissions)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Status']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
                Music.

        Returns:
            :obj:`yandex_music.Status`: Объект класса :class:`yandex_music.Status`.
        """
        if not data:
            return None

        data = super(Status, cls).de_json(data, client)
        from yandex_music import Account, Permissions, Plus, Subscription
        data['account'] = Account.de_json(data.get('account'), client)
        data['permissions'] = Permissions.de_json(data.get('permissions'), client)
        data['subscription'] = Subscription.de_json(data.get('subscription'), client)
        data['plus'] = Plus.de_json(data.get('plus'), client)

        return cls(client=client, **data)
