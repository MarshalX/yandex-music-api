from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, CombinedSessionItem, JSONType


@model
class CombinedSession(YandexMusicModel):
    """Класс, представляющий комбинированную сессию радио (треки и клипы).

    Note:
        Поле `session_id` приходит только при создании сессии.

    Attributes:
        session_id (:obj:`str`, optional): Уникальный идентификатор сессии.
        batch_id (:obj:`str`, optional): Уникальный идентификатор партии элементов.
        pumpkin (:obj:`bool`, optional): TODO.
        list (:obj:`list` из :obj:`yandex_music.CombinedSessionItem`, optional): Элементы сессии.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    session_id: Optional[str] = None
    batch_id: Optional[str] = None
    pumpkin: Optional[bool] = None
    list: Optional[List['CombinedSessionItem']] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.session_id, self.batch_id)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['CombinedSession']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.CombinedSession`: Комбинированная сессия радио.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music import CombinedSessionItem

        cls_data['list'] = CombinedSessionItem.de_list(cls_data.get('list'), client)

        return cls(client=client, **cls_data)
