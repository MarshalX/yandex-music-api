from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Account, Alert, ClientType, JSONType, Permissions, Plus, StationData, Subscription


@model
class Status(YandexMusicModel):
    """Класс, представляющий подробную информацию об аккаунте пользователя.

    Attributes:
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
        pretrial_active (:obj:`bool`, optional): TODO.
        userhash (:obj:`str`, optional): Хэш-код идентификатора пользователя.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    account: Optional['Account']
    permissions: Optional['Permissions']
    advertisement: Optional[str] = None
    subscription: Optional['Subscription'] = None
    cache_limit: Optional[int] = None
    subeditor: Optional[bool] = None
    subeditor_level: Optional[int] = None
    plus: Optional['Plus'] = None
    default_email: Optional[str] = None
    skips_per_hour: Optional[int] = None
    station_exists: Optional[bool] = None
    station_data: Optional['StationData'] = None
    bar_below: Optional['Alert'] = None
    premium_region: Optional[int] = None
    experiment: Optional[int] = None
    pretrial_active: Optional[bool] = None
    userhash: Optional[str] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.account, self.permissions)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['Status']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Status`: Информация об аккаунте пользователя.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music import Account, Alert, Permissions, Plus, StationData, Subscription

        cls_data['account'] = Account.de_json(data.get('account'), client)
        cls_data['permissions'] = Permissions.de_json(data.get('permissions'), client)
        cls_data['subscription'] = Subscription.de_json(data.get('subscription'), client)
        cls_data['plus'] = Plus.de_json(data.get('plus'), client)
        cls_data['station_data'] = StationData.de_json(data.get('station_data'), client)
        cls_data['bar_below'] = Alert.de_json(data.get('bar_below'), client)

        return cls(client=client, **cls_data)  # type: ignore
