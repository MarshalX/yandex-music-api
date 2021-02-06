from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client


class RenewableRemainder(YandexMusicObject):
    """Класс, представляющий напоминания о продлении подписки.

    Note:
        Присутствует только тогда, когда автопродление отключено.

    Attributes:
        days (:obj:`int`): Количество дней (до окончания подписки, по всей видимости).
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.

    Args:
        days (:obj:`int`): Количество дней (до окончания подписки, по всей видимости).
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self, days: int, client: Optional['Client'] = None, **kwargs) -> None:
        self.days = days

        self.client = client
        self._id_attrs = (self.days,)

        super().handle_unknown_kwargs(self, **kwargs)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['RenewableRemainder']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.PassportPhone`: Напоминание о продлении подписки.
        """
        if not data:
            return None

        data = super(RenewableRemainder, cls).de_json(data, client)

        return cls(client=client, **data)
