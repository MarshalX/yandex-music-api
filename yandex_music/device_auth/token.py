from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType


@model
class OAuthToken(YandexMusicModel):
    """Класс, представляющий OAuth-токен, полученный через Device Flow.

    Attributes:
        access_token (:obj:`str`): OAuth-токен доступа.
        refresh_token (:obj:`str`, optional): Токен для обновления access_token.
        expires_in (:obj:`int`, optional): Срок жизни access_token в секундах.
        token_type (:obj:`str`, optional): Тип токена (обычно ``bearer``).
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    access_token: str
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None
    token_type: Optional[str] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.access_token,)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['OAuthToken']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.OAuthToken` | :obj:`None`: OAuth-токен.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        return cls(client=client, **cls_data)
