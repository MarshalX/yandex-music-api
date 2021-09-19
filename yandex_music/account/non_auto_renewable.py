from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicObject
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client


@model
class NonAutoRenewable(YandexMusicObject):
    """Класс, представляющий отключённое автопродление.

    Attributes:
        start (:obj:`str`): Дата начала подписки.
        end (:obj:`str`): Дата окончания подписки.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    start: str
    end: str
    client: Optional['Client'] = None

    def __post_init__(self):
        self._id_attrs = (self.start, self.end)

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
