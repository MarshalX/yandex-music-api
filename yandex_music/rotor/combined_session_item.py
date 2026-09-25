from typing import TYPE_CHECKING, Optional, Union

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, Clip, JSONType, Track


@model
class CombinedSessionItem(YandexMusicModel):
    """Класс, представляющий элемент комбинированной сессии радио.

    Note:
        В зависимости от поля `type`, в поле `data` будет объект соответствующего типа:
        `CLIP`: :class:`yandex_music.Clip`, `TRACK`: :class:`yandex_music.Track`.

    Attributes:
        type (:obj:`str`, optional): Тип элемента.
        data (:obj:`yandex_music.Clip` | :obj:`yandex_music.Track`, optional): Содержимое элемента.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    type: Optional[str] = None
    data: Optional[Union['Clip', 'Track']] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.type, self.data)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['CombinedSessionItem']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.CombinedSessionItem`: Элемент комбинированной сессии радио.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music import Clip, Track

        item_type = str(cls_data.get('type') or '').upper()
        if item_type == 'CLIP':
            cls_data['data'] = Clip.de_json(cls_data.get('data'), client)
        elif item_type == 'TRACK':
            cls_data['data'] = Track.de_json(cls_data.get('data'), client)
        else:
            cls_data['data'] = None

        return cls(client=client, **cls_data)
