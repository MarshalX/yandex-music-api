from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicObject
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client, Status


@model
class PromoCodeStatus(YandexMusicObject):
    """Класс, представляющий статус активации промо-кода.

    Attributes:
        status (:obj:`str`): Статус операции.
        status_desc (:obj:`str`): Описание статуса.
        account_status (:obj:`yandex_music.Status`): Информация об аккаунте пользователя.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    status: str
    status_desc: str
    account_status: Optional['Status']
    client: Optional['Client'] = None

    def __post_init__(self):
        self._id_attrs = (self.status, self.status_desc, self.account_status)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['PromoCodeStatus']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.PromoCodeStatus`: Статус активации промо-кода.
        """
        if not data:
            return None

        data = super(PromoCodeStatus, cls).de_json(data, client)
        from yandex_music import Status

        data['account_status'] = Status.de_json(data.get('account_status'), client)

        return cls(client=client, **data)
