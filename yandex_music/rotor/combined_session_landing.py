from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, CombinedSessionItem, JSONType


@model
class CombinedSessionLanding(YandexMusicModel):
    """Класс, представляющий витрину комбинированной сессии радио (например, «Время клипов»).

    Attributes:
        title (:obj:`str`, optional): Заголовок.
        description (:obj:`str`, optional): Описание.
        button (:obj:`str`, optional): Текст кнопки.
        list (:obj:`list` из :obj:`yandex_music.CombinedSessionItem`, optional): Элементы витрины.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    title: Optional[str] = None
    description: Optional[str] = None
    button: Optional[str] = None
    list: Optional[List['CombinedSessionItem']] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.title, self.list)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['CombinedSessionLanding']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.CombinedSessionLanding`: Витрина комбинированной сессии радио.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music import CombinedSessionItem

        cls_data['list'] = CombinedSessionItem.de_list(cls_data.get('list'), client)

        return cls(client=client, **cls_data)
