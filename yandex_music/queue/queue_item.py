from typing import TYPE_CHECKING, Any, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, Context, JSONType, Queue


@model
class QueueItem(YandexMusicModel):
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
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.id,)

    def fetch_queue(self, *args: Any, **kwargs: Any) -> Optional['Queue']:
        """Сокращение для::

        client.queue(id, *args, **kwargs)
        """
        assert self.valid_client(self.client)
        return self.client.queue(self.id, *args, **kwargs)

    async def fetch_queue_async(self, *args: Any, **kwargs: Any) -> Optional['Queue']:
        """Сокращение для::

        await client.queue(id, *args, **kwargs)
        """
        assert self.valid_async_client(self.client)
        return await self.client.queue(self.id, *args, **kwargs)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['QueueItem']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.QueueItem`: Очередь в списке.
        """
        if not cls.is_dict_model_data(data):
            return None

        from yandex_music import Context

        cls_data = cls.cleanup_data(data, client)
        cls_data['context'] = Context.de_json(data.get('context'), client)

        return cls(client=client, **cls_data)  # type: ignore

    # camelCase псевдонимы

    #: Псевдоним для :attr:`fetch_queue`
    fetchQueue = fetch_queue
    #: Псевдоним для :attr:`fetch_queue_async`
    fetchQueueAsync = fetch_queue_async
