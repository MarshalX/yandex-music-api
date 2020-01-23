from typing import TYPE_CHECKING, Optional, List

if TYPE_CHECKING:
    from yandex_music import Client, Shot

from yandex_music import YandexMusicObject


class ShotEvent(YandexMusicObject):
    """Класс, представляющий событие-шот перед началом следующего трека.

    Attributes:
        event_id (:obj:`str`): Уникальный идентификатор события.
        shots (:obj:`list` из :obj:`yandex_music.Shot`): Список объектов класса :class:`yandex_music.Shot`
            представляющие шоты от Алисы.
        client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
            Music.

    Args:
        event_id (:obj:`str`): Уникальный идентификатор события.
        shots (:obj:`list` из :obj:`yandex_music.Shot`): Список объектов класса :class:`yandex_music.Shot`
            представляющие шоты от Алисы.
        client (:obj:`yandex_music.Client`, optional): Объект класса :class:`yandex_music.Client` представляющий клиент
            Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 event_id: str,
                 shots: List['Shot'],
                 client: Optional['Client'] = None,
                 **kwargs):
        self.event_id = event_id
        self.shots = shots

        self.client = client
        self._id_attrs = (self.event_id, self.shots)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['ShotEvent']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
                Music.

        Returns:
            :obj:`yandex_music.ShotEvent`: Объект класса :class:`yandex_music.ShotEvent`.
        """
        if not data:
            return None

        data = super(ShotEvent, cls).de_json(data, client)
        from yandex_music import Shot
        data['shots'] = Shot.de_list(data.get('shots'), client)

        return cls(client=client, **data)
