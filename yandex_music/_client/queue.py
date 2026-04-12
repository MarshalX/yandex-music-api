##############################################################################################
# THIS IS AUTO GENERATED COPY OF yandex_music/_client_async/queue.py. DON'T EDIT IT BY HANDS #
##############################################################################################

from typing import TYPE_CHECKING, Any, List, Optional, Union

from yandex_music import Queue, QueueItem
from yandex_music._client import log
from yandex_music._client_base import ClientBase

if TYPE_CHECKING:
    from yandex_music.utils.request import Request


class QueueMixin(ClientBase):
    """Миксин для методов, связанных с очередью прослушивания."""

    _request: 'Request'

    @log
    def queues_list(self, device: Optional[str] = None, *args: Any, **kwargs: Any) -> List[QueueItem]:
        """Получение всех очередей треков с разных устройств для синхронизации между ними.

        Note:
            Именно к `device` привязывается очередь. На одном устройстве может быть создана одна очередь.

            Аргумент `device` имеет следующий формат: `ключ=значение; ключ2=значение2`. Обязательные паля указы в
            значении по умолчанию.

        Args:
            device (:obj:`str`, optional): Содержит информацию об устройстве с которого выполняется запрос.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`list` из :obj:`yandex_music.QueueItem`: Элементы очереди всех устройств.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        if not device:
            device = self.device

        url = f'{self.base_url}/queues'

        self._request.headers['X-Yandex-Music-Device'] = device
        result = self._request.get(url, *args, **kwargs)

        return QueueItem.de_list(result.get('queues'), self)

    @log
    def queue(self, queue_id: str, *args: Any, **kwargs: Any) -> Optional[Queue]:
        """Получение информации об очереди треков и самих треков в ней.

        Args:
            queue_id (:obj:`str`): Уникальный идентификатор очереди.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`yandex_music.Queue`: Очередь или :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        url = f'{self.base_url}/queues/{queue_id}'

        result = self._request.get(url, *args, **kwargs)

        return Queue.de_json(result, self)

    @log
    def queue_update_position(self, queue_id: str, current_index: int, device: Optional[str] = None, **kwargs) -> bool:
        """Установка текущего индекса проигрываемого трека в очереди треков.

        Note:
            Изменить можно только у той очереди, которая была создана с переданного `device`!

        Args:
            queue_id (:obj:`str`): Уникальный идентификатор очереди.
            current_index (:obj:`int`): Текущий индекс.
            device (:obj:`str`, optional): Содержит информацию об устройстве с которого выполняется запрос.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`bool`: :obj:`True` при успешном выполнении запроса, иначе :obj:`False`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        if not device:
            device = self.device

        url = f'{self.base_url}/queues/{queue_id}/update-position'

        self._request.headers['X-Yandex-Music-Device'] = device
        result = self._request.post(url, {'isInteractive': False}, params={'currentIndex': current_index}, **kwargs)

        return result.get('status') == 'ok'

    @log
    def queue_create(
        self, queue: Union[Queue, str], device: Optional[str] = None, *args: Any, **kwargs: Any
    ) -> Optional[str]:
        """Создание новой очереди треков.

        Args:
            queue (:obj:`yandex_music.Queue` | :obj:`str`): Объект очереди или JSON строка с этим объектом.
            device (:obj:`str`, optional): Содержит информацию об устройстве с которого выполняется запрос.
            *args: Произвольные аргументы (будут переданы в запрос).
            **kwargs: Произвольные именованные аргументы (будут переданы в запрос).

        Returns:
            :obj:`str`: Вернёт уникальный идентификатор созданной очереди, иначе :obj:`None`.

        Raises:
            :class:`yandex_music.exceptions.YandexMusicError`: Базовое исключение библиотеки.
        """
        if not device:
            device = self.device

        if isinstance(queue, Queue):
            queue = queue.to_json(True)

        url = f'{self.base_url}/queues'

        self._request.headers['X-Yandex-Music-Device'] = device
        result = self._request.post(url, queue, *args, **kwargs)

        return result.get('id')

    # camelCase псевдонимы

    #: Псевдоним для :attr:`queues_list`
    queuesList = queues_list
    #: Псевдоним для :attr:`queue_update_position`
    queueUpdatePosition = queue_update_position
    #: Псевдоним для :attr:`queue_create`
    queueCreate = queue_create
