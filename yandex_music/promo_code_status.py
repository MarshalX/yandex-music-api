from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from yandex_music import Client, Status

from yandex_music import YandexMusicObject


class PromoCodeStatus(YandexMusicObject):
    """Класс представляющий статус активации промо-кода.

    Attributes:
        status (:obj:`str`): Статус операции.
        status_desc (:obj:`str`): Описание статуса.
        account_status (:obj:`yandex_music.Status`): Объект класса :class:`yandex_music.Status` представляющий подробную
            информацию об аккаунте пользователя.
        client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
            Music.

    Args:
        status (:obj:`str`): Статус операции.
        status_desc (:obj:`str`): Описание статуса.
        account_status (:obj:`yandex_music.Status`): Объект класса :class:`yandex_music.Status` представляющий подробную
            информацию об аккаунте пользователя.
        client (:obj:`yandex_music.Client`, optional): Объект класса :class:`yandex_music.Client` представляющий клиент
            Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 status: str,
                 status_desc: str,
                 account_status: Optional['Status'],
                 client: Optional['Client'] = None,
                 **kwargs):
        self.status = status
        self.status_desc = status_desc
        self.account_status = account_status

        self.client = client
        self._id_attrs = (self.status, self.status_desc, self.account_status)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['PromoCodeStatus']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
                Music.

        Returns:
            :obj:`yandex_music.PromoCodeStatus`: Объект класса :class:`yandex_music.PromoCodeStatus`.
        """
        if not data:
            return None

        data = super(PromoCodeStatus, cls).de_json(data, client)
        from yandex_music import Status
        data['account_status'] = Status.de_json(data.get('account_status'), client)

        return cls(client=client, **data)
