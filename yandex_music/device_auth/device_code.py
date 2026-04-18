from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType


@model
class DeviceCode(YandexMusicModel):
    """Класс, представляющий код устройства для OAuth Device Flow.

    Attributes:
        device_code (:obj:`str`): Непрозрачный идентификатор устройства для опроса токена.
        user_code (:obj:`str`): Код, который пользователь вводит на странице подтверждения.
        verification_url (:obj:`str`): URL страницы подтверждения.
        expires_in (:obj:`int`): Через сколько секунд истекает device_code.
        interval (:obj:`int`): Рекомендованный сервером интервал опроса в секундах.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    device_code: str
    user_code: str
    verification_url: str
    expires_in: int
    interval: int
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.device_code, self.user_code)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['DeviceCode']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.DeviceCode` | :obj:`None`: Код устройства.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        return cls(client=client, **cls_data)
