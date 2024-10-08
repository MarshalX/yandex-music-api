from dataclasses import field
from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import AutoRenewable, ClientType, JSONType, NonAutoRenewable, Operator, RenewableRemainder


@model
class Subscription(YandexMusicModel):
    """Класс, представляющий информацию о подписках пользователя.

    Attributes:
        non_auto_renewable_remainder (:obj:`yandex_music.RenewableRemainder`): Напоминание о продлении.
        auto_renewable (:obj:`list` из :obj:`yandex_music.AutoRenewable`, optional): Автопродление.
        family_auto_renewable (:obj:`list` из :obj:`yandex_music.AutoRenewable`): Автопродление семейной подписки.
        operator (:obj:`list` из :obj:`yandex_music.Operator`, optional): Услуги сотового оператора.
        non_auto_renewable (:obj:`yandex_music.NonAutoRenewable`, optional): Отключённое автопродление.
        can_start_trial (:obj:`bool`, optional): Есть ли возможность начать пробный период.
        mcdonalds (:obj:`bool`, optional): mcdonalds TODO.
        end (:obj:`str`, optional): Дата окончания.
        had_any_subscription (:obj:'bool'): Наличие какой-либо подписки в прошлом.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    non_auto_renewable_remainder: 'RenewableRemainder'
    auto_renewable: List['AutoRenewable']
    family_auto_renewable: List['AutoRenewable']
    had_any_subscription: bool
    operator: List['Operator'] = field(default_factory=list)
    non_auto_renewable: Optional['NonAutoRenewable'] = None
    can_start_trial: Optional[bool] = None
    mcdonalds: Optional[bool] = None
    end: Optional[str] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.non_auto_renewable_remainder, self.auto_renewable, self.family_auto_renewable)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['Subscription']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Subscription`: Информация о подписках пользователя.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music import AutoRenewable, NonAutoRenewable, Operator, RenewableRemainder

        cls_data['auto_renewable'] = AutoRenewable.de_list(data.get('auto_renewable'), client)
        cls_data['family_auto_renewable'] = AutoRenewable.de_list(data.get('family_auto_renewable'), client)
        cls_data['non_auto_renewable_remainder'] = RenewableRemainder.de_json(
            data.get('non_auto_renewable_remainder'), client
        )
        cls_data['non_auto_renewable'] = NonAutoRenewable.de_json(data.get('non_auto_renewable'), client)
        cls_data['operator'] = Operator.de_list(data.get('operator'), client)

        return cls(client=client, **cls_data)  # type: ignore
