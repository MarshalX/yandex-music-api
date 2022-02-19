from typing import TYPE_CHECKING, Optional, List

from yandex_music import YandexMusicObject
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client


@model
class Cover(YandexMusicObject):
    """Класс, представляющий обложку.

    Attributes:
        type (:obj:`str`, optional): Тип обложки.
        uri (:obj:`str`, optional): Ссылка на изображение.
        items_uri (:obj:`str`, optional): Список ссылок на изображения.
        dir (:obj:`str`, optional): Директория хранения изображения на сервере.
        version (:obj:`str`, optional): Версия.
        is_custom (:obj:`bool`, optional): Является ли обложка пользовательской.
        custom (:obj:`bool`, optional): Является ли обложка пользовательской.
        prefix (:obj:`str`, optional): Уникальный идентификатор.
        copyright_name (:obj:`str`, optional): Название владельца авторским правом.
        copyright_cline (:obj:`str`, optional): Владелец прав на музыку (автор текста и т.д.), а не её записи.
        error (:obj:`str`, optional): Сообщение об ошибке.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    type: Optional[str] = None
    uri: Optional[str] = None
    items_uri: Optional[str] = None
    dir: Optional[str] = None
    version: Optional[str] = None
    custom: Optional[bool] = None
    is_custom: Optional[bool] = None
    copyright_name: Optional[str] = None
    copyright_cline: Optional[str] = None
    prefix: Optional[str] = None
    error: Optional[str] = None
    client: Optional['Client'] = None

    def __post_init__(self):
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

    async def download_async(self, filename: str, index: int = 0, size: str = '200x200') -> None:
        """Загрузка обложки.

        Args:
            filename (:obj:`str`): Путь для сохранения файла с названием и расширением.
            index (:obj:`int`, optional): Индекс элемента в списке ссылок на обложки если нет `self.uri`.
            size (:obj:`str`, optional): Размер изображения.
        """
        uri = self.uri or self.items_uri[index]

        await self.client.request.download(f'https://{uri.replace("%%", size)}', filename)

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

    # camelCase псевдонимы

    #: Псевдоним для :attr:`download_async`
    downloadAsync = download_async
