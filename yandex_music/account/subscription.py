from typing import TYPE_CHECKING, Optional, List

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client, AutoRenewable


class Subscription(YandexMusicObject):
    """Класс, представляющий информацию о подписках пользователя.

    Attributes:
        auto_renewable (:obj:`list` из :obj:`yandex_music.AutoRenewable`): Автопродление.
        can_start_trial (:obj:`bool`): Есть ли возможность начать пробный период.
        mcdonalds (:obj:`bool`): mcdonalds TODO.
        end (:obj:`str`): Дата окончания.
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.

    Args:
        auto_renewable (:obj:`list` из :obj:`yandex_music.AutoRenewable`, optional): Автопродление.
        can_start_trial (:obj:`bool`, optional): Есть ли возможность начать пробный период.
        mcdonalds (:obj:`bool`, optional): mcdonalds TODO.
        end (:obj:`str`, optional): Дата окончания.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 auto_renewable: List['AutoRenewable'] = None,
                 can_start_trial: Optional[bool] = None,
                 mcdonalds: Optional[bool] = None,
                 end: Optional[str] = None,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        super().handle_unknown_kwargs(self, **kwargs)

        self.auto_renewable = auto_renewable
        self.can_start_trial = can_start_trial
        self.mcdonalds = mcdonalds
        self.end = end

        self.client = client
        self._id_attrs = (self.auto_renewable,)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Subscription']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Subscription`: Информация о подписках пользователя.
        """
        if not data:
            return None

        data = super(Subscription, cls).de_json(data, client)
        from yandex_music import AutoRenewable
        data['auto_renewable'] = AutoRenewable.de_list(data.get('auto_renewable'), client)

        return cls(client=client, **data)
