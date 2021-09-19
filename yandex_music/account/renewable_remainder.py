from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicObject
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client


@model
class RenewableRemainder(YandexMusicObject):
    """Класс, представляющий напоминания о продлении подписки.

    Note:
        Присутствует только тогда, когда автопродление отключено.

    Attributes:
        days (:obj:`int`): Количество дней (до окончания подписки, по всей видимости).
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    days: int
    client: Optional['Client'] = None

    def __post_init__(self):
        self._id_attrs = (self.days,)

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
