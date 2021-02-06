from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client


class NonAutoRenewable(YandexMusicObject):
    """Класс, представляющий отключённое автопродление.

    Attributes:
        start (:obj:`str`): Дата начала подписки.
        end (:obj:`str`): Дата окончания подписки.
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.

    Args:
        start (:obj:`str`): Дата начала подписки.
        end (:obj:`str`): Дата окончания подписки.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self, start: str, end: str, client: Optional['Client'] = None, **kwargs) -> None:
        self.start = start
        self.end = end

        self.client = client
        self._id_attrs = (self.start, self.end)

        super().handle_unknown_kwargs(self, **kwargs)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['NonAutoRenewable']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.NonAutoRenewable`: Отключённое автопродление.
        """
        if not data:
            return None

        data = super(NonAutoRenewable, cls).de_json(data, client)

        return cls(client=client, **data)
