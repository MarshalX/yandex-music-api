from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType
    from yandex_music.track.fade import Fade


@model
class SmartPreviewParams(YandexMusicModel):
    """Класс, представляющий параметры умного превью трека.

    Attributes:
        duration_ms (:obj:`int`, optional): Длительность превью в миллисекундах.
        fade (:obj:`yandex_music.Fade`, optional): Параметры затухания превью.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    duration_ms: Optional[int] = None
    fade: Optional['Fade'] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.duration_ms, self.fade)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['SmartPreviewParams']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.SmartPreviewParams`: Параметры умного превью трека.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music.track.fade import Fade

        cls_data['fade'] = Fade.de_json(cls_data.get('fade'), client)

        return cls(client=client, **cls_data)
