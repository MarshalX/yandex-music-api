from typing import TYPE_CHECKING, Optional, List

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client


class Cover(YandexMusicObject):
    """Класс, представляющий обложку.

    Attributes:
        type (:obj:`str`): Тип обложки.
        uri (:obj:`str`): Ссылка на изображение.
        items_uri (:obj:`str`): Список ссылок на изображения.
        dir (:obj:`str`): Директория хранения изображения на сервере.
        version (:obj:`str`): Версия.
        custom (:obj:`bool`): Является ли обложка пользовательской.
        prefix (:obj:`str`): Уникальный идентификатор.
        error (:obj:`str`): Сообщение об ошибке.
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.

    Args:
        type_ (:obj:`str`, optional): Тип обложки.
        uri (:obj:`str`, optional): Ссылка на изображение.
        items_uri (:obj:`str`, optional): Список ссылок на изображения.
        dir_ (:obj:`str`, optional): Директория хранения изображения на сервере.
        version (:obj:`str`, optional): Версия.
        custom (:obj:`bool`, optional): Является ли обложка пользовательской.
        prefix (:obj:`str`, optional): Уникальный идентификатор.
        error (:obj:`str`, optional): Сообщение об ошибке.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 type_: Optional[str] = None,
                 uri: Optional[str] = None,
                 items_uri: Optional[str] = None,
                 dir_: Optional[str] = None,
                 version: Optional[str] = None,
                 custom: Optional[bool] = None,
                 prefix: Optional[str] = None,
                 error: Optional[str] = None,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        super().handle_unknown_kwargs(self, **kwargs)

        self.type = type_
        self.uri = uri
        self.items_uri = items_uri
        self.prefix = prefix
        self.dir = dir_
        self.version = version
        self.custom = custom
        self.error = error

        self.client = client
        self._id_attrs = (self.prefix, self.version, self.uri, self.items_uri)

    def download(self, filename: str, index: int = 0, size: str = '200x200') -> None:
        """Загрузка обложки.

        Args:
            filename (:obj:`str`): Путь для сохранения файла с названием и расширением.
            index (:obj:`int`, optional): Индекс элемента в списке ссылок на обложки если нет `self.uri`.
            size (:obj:`str`, optional): Размер изображения.
        """
        uri = self.uri or self.items_uri[index]

        self.client.request.download(f'https://{uri.replace("%%", size)}', filename)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Cover']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Cover`: Обложка.
        """
        if not data:
            return None

        data = super(Cover, cls).de_json(data, client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data: dict, client: 'Client') -> List['Cover']:
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.Cover`: Обложки.
        """
        if not data:
            return []

        covers = list()
        for cover in data:
            covers.append(cls.de_json(cover, client))

        return covers
