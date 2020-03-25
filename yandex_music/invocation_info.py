from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client


class InvocationInfo(YandexMusicObject):
    """Класс, представляющий информацию о запросе.

    Attributes:
        hostname (:obj:`str`): Имя удалённого сервера.
        req_id (:obj:`str`): Номер запроса.
        exec_duration_millis (:obj:`str`): Время выполнения в миллисекундах.
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.

    Args:
        hostname (:obj:`str`): Имя удалённого сервера.
        req_id (:obj:`str`): Номер запроса.
        exec_duration_millis (:obj:`str`, optional): Время выполнения в миллисекундах.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 hostname: str,
                 req_id: str,
                 exec_duration_millis: Optional[int] = None,
                 client: Optional['Client'] = None,
                 **kwargs):
        self.hostname = hostname
        self.req_id = req_id

        self.exec_duration_millis = exec_duration_millis

        self.client = client
        self._id_attrs = (self.hostname, self.req_id)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['InvocationInfo']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.InvocationInfo`: Информация о запросе.
        """
        if not data:
            return None

        data = super(InvocationInfo, cls).de_json(data, client)

        return cls(client=client, **data)
