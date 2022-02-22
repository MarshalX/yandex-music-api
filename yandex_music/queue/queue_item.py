from typing import List, TYPE_CHECKING, Optional

from yandex_music import YandexMusicObject
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client, Context, Queue


@model
class QueueItem(YandexMusicObject):
    """Класс, представляющий очередь треков в списке очередей устройств.

    Attributes:
        id (:obj:`str`): Уникальный идентификатор очереди.
        context (:obj:`yandex_music.Context` | :obj:`None`): Объект по которому построена очередь.
        modified (:obj:`str`): Дата последнего изменения.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    id: str
    context: Optional['Context']
    modified: str
    client: Optional['Client'] = None

    def __post_init__(self):
        self._id_attrs = (self.id,)

    def fetch_queue(self, *args, **kwargs) -> Optional['Queue']:
        """Сокращение для::

        client.queue(id, *args, **kwargs)
        """
        return self.client.queue(self.id, *args, **kwargs)

    async def fetch_queue_async(self, *args, **kwargs) -> Optional['Queue']:
        """Сокращение для::

        await client.queue(id, *args, **kwargs)
        """
        return await self.client.queue(self.id, *args, **kwargs)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['QueueItem']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.QueueItem`: Очередь в списке.
        """
        if not data:
            return None

        from yandex_music import Context

        data = super(QueueItem, cls).de_json(data, client)
        data['context'] = Context.de_json(data.get('context'), client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data: dict, client: 'Client') -> List['QueueItem']:
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.QueueItem`: Список очередей всех устройств.
        """
        if not data:
            return []

        return [cls.de_json(queue, client) for queue in data]

    # camelCase псевдонимы

    #: Псевдоним для :attr:`fetch_queue`
    fetchQueue = fetch_queue
    #: Псевдоним для :attr:`fetch_queue_async`
    fetchQueueAsync = fetch_queue_async
