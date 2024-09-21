from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType, Shot


@model
class ShotEvent(YandexMusicModel):
    """Класс, представляющий событие-шот перед началом следующего трека.

    Attributes:
        event_id (:obj:`str`): Уникальный идентификатор события.
        shots (:obj:`list` из :obj:`yandex_music.Shot`): Шоты от Алисы.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    event_id: str
    shots: List['Shot']
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.event_id, self.shots)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['ShotEvent']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.ShotEvent`: Событие-шот перед началом следующего трека.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music import Shot

        cls_data['shots'] = Shot.de_list(data.get('shots'), client)

        return cls(client=client, **cls_data)  # type: ignore
