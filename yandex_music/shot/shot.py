from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType, ShotData


@model
class Shot(YandexMusicModel):
    """Класс, представляющий шот от Алисы.

    Note:
        Известные значения поля `status`: `ready`.

    Attributes:
        order (:obj:`int`): Порядковый номер при воспроизведении.
        played (:obj:`bool`): Был ли проигран шот.
        shot_data (:obj:`yandex_music.ShotData`): Основная информация о шоте.
        shot_id (:obj:`str`): Уникальный идентификатор шота.
        status (:obj:`str`): Статус шота.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    order: int
    played: bool
    shot_data: 'ShotData'
    shot_id: str
    status: str
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.order, self.played, self.shot_data, self.shot_id, self.status)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['Shot']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Shot`: Шот от Алисы.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music import ShotData

        cls_data['shot_data'] = ShotData.de_json(data.get('shot_data'), client)

        return cls(client=client, **cls_data)  # type: ignore
