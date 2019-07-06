from datetime import datetime

from yandex_music import YandexMusicObject


class Subscription(YandexMusicObject):
    """Класс предоставляющий информацию о подписках пользователя.

    Attributes:
        auto_renewable (:obj:`list` из :obj:`yandex_music.AutoRenewable`): Список объектов класса
            :class:`yandex_music.AutoRenewable` представляющих автопродление.
        can_start_trial (:obj:`bool`): Есть ли возможность начать пробный период.
        mcdonalds (:obj:`bool`): mcdonalds TODO.
        end (:obj:`datetime.datetime`): Дата окончания.
        client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
            Music.

    Args:
        auto_renewable (:obj:`list` из :obj:`yandex_music.AutoRenewable`, optional): Список объектов класса
            :class:`yandex_music.AutoRenewable` представляющих автопродление.
        can_start_trial (:obj:`bool`, optional): Есть ли возможность начать пробный период.
        mcdonalds (:obj:`bool`, optional): mcdonalds TODO.
        end (:obj:`str`, optional): Дата окончания.
        client (:obj:`yandex_music.Client`, optional): Объект класса :class:`yandex_music.Client` представляющий клиент
            Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 auto_renewable=None,
                 can_start_trial=None,
                 mcdonalds=None,
                 end=None,
                 client=None,
                 **kwargs):
        self.auto_renewable = auto_renewable
        self.can_start_trial = can_start_trial
        self.mcdonalds = mcdonalds
        self.end = datetime.fromisoformat(end) if end else end

        self.client = client

    @classmethod
    def de_json(cls, data, client):
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
                Music.

        Returns:
            :obj:`yandex_music.Subscription`: Объект класса :class:`yandex_music.Subscription`.
        """
        if not data:
            return None

        data = super(Subscription, cls).de_json(data, client)
        from yandex_music import AutoRenewable
        data['auto_renewable'] = AutoRenewable.de_list(data.get('auto_renewable'), client)

        return cls(client=client, **data)
