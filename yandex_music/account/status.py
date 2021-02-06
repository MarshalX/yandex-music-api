from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client, Account, Permissions, Subscription, Plus, StationData, Alert


class Status(YandexMusicObject):
    """Класс, представляющий подробную информацию об аккаунте пользователя.

    Attributes:
        account (:obj:`yandex_music.Account`): Основная информация об аккаунте.
        permissions (:obj:`yandex_music.Permissions`): Информация о правах пользователя.
        advertisement (:obj:`str`): Рекламное объявление.
        subscription (:obj:`yandex_music.Subscription`): Информация о подписках.
        cache_limit (:obj:`int`): Максимальное количество загруженных треков.
        subeditor (:obj:`bool`): Наличие статуса модератора проверки корректности информации.
        subeditor_level (:obj:`int`): Уровень статуса модератора.
        plus (:obj:`yandex_music.Plus`): Информация о Plus подписке.
        default_email (:obj:`str`): Основной e-mail адрес аккаунта.
        skips_per_hour (:obj:`int`): Количество переключение треков на радио в час.
        station_exists (:obj:`bool`): Наличие личной станции.
        station_data (:obj:`yandex_music.StationData`): Информация о личной станции.
        bar_below (:obj:`yandex_music.Alert`): Блок с предупреждениями о конце подписке и подарках.
        premium_region (:obj:`int`): Регион TODO.
        experiment (:obj:`int`): Включенная новая фича на аккаунте (её ID) TODO.
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.

    Args:
        account (:obj:`yandex_music.Account`): Основная информация об аккаунте
        permissions (:obj:`yandex_music.Permissions`): Информация о правах пользователя.
        advertisement (:obj:`str`, optional): Рекламное объявление.
        subscription (:obj:`yandex_music.Subscription`, optional): Информация о подписках.
        cache_limit (:obj:`int`, optional): Максимальное количество загруженных треков.
        subeditor (:obj:`bool`, optional): Наличие статуса модератора проверки корректности информации.
        subeditor_level (:obj:`int`, optional): Уровень статуса модератора.
        plus (:obj:`yandex_music.Plus`, optional): Информация о Plus подписке.
        default_email (:obj:`str`, optional): Основной e-mail адрес аккаунта.
        skips_per_hour (:obj:`int`, optional): Количество переключение треков на радио в час.
        station_exists (:obj:`bool`, optional): Наличие личной станции.
        station_data (:obj:`yandex_music.StationData`, optional): Информация о личной станции.
        bar_below (:obj:`yandex_music.Alert`, optional): Блок с предупреждениями о конце подписке и подарках.
        premium_region (:obj:`int`, optional): Регион TODO.
        experiment (:obj:`int`, optional): Включенная новая фича на аккаунте (её ID) TODO.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(
        self,
        account: Optional['Account'],
        permissions: Optional['Permissions'],
        advertisement: Optional[str] = None,
        subscription: Optional['Subscription'] = None,
        cache_limit: Optional[int] = None,
        subeditor: Optional[bool] = None,
        subeditor_level: Optional[int] = None,
        plus: Optional['Plus'] = None,
        default_email: Optional[str] = None,
        skips_per_hour: Optional[int] = None,
        station_exists: Optional[bool] = None,
        station_data: Optional['StationData'] = None,
        bar_below: Optional['Alert'] = None,
        premium_region: Optional[int] = None,
        experiment: Optional[int] = None,
        client: Optional['Client'] = None,
        **kwargs,
    ) -> None:
        self.account = account
        self.permissions = permissions

        self.advertisement = advertisement
        self.subscription = subscription
        self.cache_limit = cache_limit
        self.subeditor = subeditor
        self.subeditor_level = subeditor_level
        self.plus = plus
        self.default_email = default_email
        self.skips_per_hour = skips_per_hour
        self.station_exists = station_exists
        self.station_data = station_data
        self.bar_below = bar_below
        self.premium_region = premium_region
        self.experiment = experiment

        self.client = client
        self._id_attrs = (self.account, self.permissions)

        super().handle_unknown_kwargs(self, **kwargs)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Status']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Status`: Информация об аккаунте пользователя.
        """
        if not data:
            return None

        data = super(Status, cls).de_json(data, client)
        from yandex_music import Account, Permissions, Plus, Subscription, StationData, Alert

        data['account'] = Account.de_json(data.get('account'), client)
        data['permissions'] = Permissions.de_json(data.get('permissions'), client)
        data['subscription'] = Subscription.de_json(data.get('subscription'), client)
        data['plus'] = Plus.de_json(data.get('plus'), client)
        data['station_data'] = StationData.de_json(data.get('station_data'), client)
        data['bar_below'] = Alert.de_json(data.get('bar_below'), client)

        return cls(client=client, **data)
