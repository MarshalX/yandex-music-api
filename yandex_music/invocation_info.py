from yandex_music import YandexMusicObject


class InvocationInfo(YandexMusicObject):
    """Класс представляющий информацию о запросе.

    Attributes:
        hostname (:obj:`str`): Имя удалённого сервера.
        req_id (:obj:`str`): Номер запроса.
        exec_duration_millis (:obj:`str`): Время выполнения в миллисекундах.
        client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
            Music.

    Args:
        hostname (:obj:`str`): Имя удалённого сервера.
        req_id (:obj:`str`): Номер запроса.
        exec_duration_millis (:obj:`str`, optional): Время выполнения в миллисекундах.
        client (:obj:`yandex_music.Client`, optional): Объект класса :class:`yandex_music.Client` представляющий клиент
            Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 hostname,
                 req_id,
                 exec_duration_millis=None,
                 client=None,
                 **kwargs):
        self.hostname = hostname
        self.req_id = req_id

        self.exec_duration_millis = exec_duration_millis

        self.client = client
        self._id_attrs = (self.req_id,)

    @classmethod
    def de_json(cls, data, client):
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
                Music.

        Returns:
            :obj:`yandex_music.InvocationInfo`: Объект класса :class:`yandex_music.InvocationInfo`.
        """
        if not data:
            return None

        data = super(InvocationInfo, cls).de_json(data, client)

        return cls(client=client, **data)
