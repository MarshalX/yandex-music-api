from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, Status


@model
class PromoCodeStatus(YandexMusicModel):
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
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.status, self.status_desc, self.account_status)
