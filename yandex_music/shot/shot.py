from typing import TYPE_CHECKING, Optional, List

from yandex_music import YandexMusicObject
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client, ShotData


@model
class Shot(YandexMusicObject):
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
    client: Optional['Client'] = None

    def __post_init__(self):
        self._id_attrs = (self.order, self.played, self.shot_data, self.shot_id, self.status)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Shot']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Shot`: Шот от Алисы.
        """
        if not data:
            return None

        data = super(Shot, cls).de_json(data, client)
        from yandex_music import ShotData

        data['shot_data'] = ShotData.de_json(data.get('shot_data'), client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data: dict, client: 'Client') -> List['Shot']:
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.Shot`: Шоты от Алисы.
        """
        if not data:
            return []

        shots = list()
        for shot in data:
            shots.append(cls.de_json(shot, client))

        return shots
