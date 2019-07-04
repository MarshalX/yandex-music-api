from yandex_music import YandexMusicObject


class Cover(YandexMusicObject):
    """Класс представляющий обложку.

    Attributes:
        type (:obj:`str`): Тип обложки.
        uri (:obj:`str`): Ссылка на изображение.
        items_uri (:obj:`str`): ССписок ссылок на изображения.
        dir (:obj:`str`): Директория хранения изображения на сервере.
        version (:obj:`str`): Версия.
        custom (:obj:`bool`): Является ли обложка пользовательской.
        prefix (:obj:`str`): Уникальный идентификатор.
        error (:obj:`str`): Сообщение об ошибке.
        client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
            Music.

    Args:
        type (:obj:`str`, optional): Тип обложки.
        uri (:obj:`str`, optional): Ссылка на изображение.
        items_uri (:obj:`str`, optional): ССписок ссылок на изображения.
        dir (:obj:`str`, optional): Директория хранения изображения на сервере.
        version (:obj:`str`, optional): Версия.
        custom (:obj:`bool`, optional): Является ли обложка пользовательской.
        prefix (:obj:`str`, optional): Уникальный идентификатор.
        error (:obj:`str`, optional): Сообщение об ошибке.
        client (:obj:`yandex_music.Client`, optional): Объект класса :class:`yandex_music.Client` представляющий клиент
            Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 type=None,
                 uri=None,
                 items_uri=None,
                 dir=None,
                 version=None,
                 custom=None,
                 prefix=None,
                 error=None,
                 client=None,
                 **kwargs):
        self.type = type
        self.uri = uri
        self.items_uri = items_uri
        self.prefix = prefix
        self.dir = dir
        self.version = version
        self.custom = custom
        self.error = error

        self.client = client

    def download(self, filename):
        self.client.request.download(self.uri, filename)

    @classmethod
    def de_json(cls, data, client):
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
                Music.

        Returns:
            :obj:`yandex_music.Cover`: Объект класса :class:`yandex_music.Cover`.
        """
        if not data:
            return None

        data = super(Cover, cls).de_json(data, client)

        return cls(client=client, **data)
