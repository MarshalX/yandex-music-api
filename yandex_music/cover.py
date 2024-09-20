from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client


@model
class Cover(YandexMusicModel):
    """Класс, представляющий обложку.

    Attributes:
        type (:obj:`str`, optional): Тип обложки.
        uri (:obj:`str`, optional): Ссылка на изображение.
        items_uri (:obj:`list` из :obj:`str`, optional): Список ссылок на изображения.
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
    items_uri: Optional[List[str]] = None
    dir: Optional[str] = None
    version: Optional[str] = None
    custom: Optional[bool] = None
    is_custom: Optional[bool] = None
    copyright_name: Optional[str] = None
    copyright_cline: Optional[str] = None
    prefix: Optional[str] = None
    error: Optional[str] = None
    client: Optional['Client'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.prefix, self.version, self.uri, self.items_uri)

    def get_url(self, index: int = 0, size: str = '200x200') -> str:
        """Возвращает URL обложки.

        Args:
            index (:obj:`int`, optional): Индекс элемента в списке ссылок на обложки если нет `self.uri`.
            size (:obj:`str`, optional): Размер изображения.

        Returns:
            :obj:`str`: URL адрес.
        """
        uri = self.uri or self.items_uri[index]

        return f'https://{uri.replace("%%", size)}'

    def download(self, filename: str, index: int = 0, size: str = '200x200') -> None:
        """Загрузка обложки.

        Args:
            filename (:obj:`str`): Путь для сохранения файла с названием и расширением.
            index (:obj:`int`, optional): Индекс элемента в списке ссылок на обложки если нет `self.uri`.
            size (:obj:`str`, optional): Размер изображения.
        """
        self.client.request.download(self.get_url(index, size), filename)

    async def download_async(self, filename: str, index: int = 0, size: str = '200x200') -> None:
        """Загрузка обложки.

        Args:
            filename (:obj:`str`): Путь для сохранения файла с названием и расширением.
            index (:obj:`int`, optional): Индекс элемента в списке ссылок на обложки если нет `self.uri`.
            size (:obj:`str`, optional): Размер изображения.
        """
        await self.client.request.download(self.get_url(index, size), filename)

    def download_bytes(self, index: int = 0, size: str = '200x200') -> bytes:
        """Загрузка обложки и возврат в виде байтов.

        Args:
            index (:obj:`int`, optional): Индекс элемента в списке ссылок на обложки если нет `self.uri`.
            size (:obj:`str`, optional): Размер изображения.

        Returns:
            :obj:`bytes`: Обложка в виде байтов.
        """
        return self.client.request.retrieve(self.get_url(index, size))

    async def download_bytes_async(self, index: int = 0, size: str = '200x200') -> bytes:
        """Загрузка обложки и возврат в виде байтов.

        Args:
            index (:obj:`int`, optional): Индекс элемента в списке ссылок на обложки если нет `self.uri`.
            size (:obj:`str`, optional): Размер изображения.

        Returns:
            :obj:`bytes`: Обложка в виде байтов.
        """
        return await self.client.request.retrieve(self.get_url(index, size))

    # camelCase псевдонимы

    #: Псевдоним для :attr:`get_url`
    getUrl = get_url
    #: Псевдоним для :attr:`download_async`
    downloadAsync = download_async
    #: Псевдоним для :attr:`download_bytes`
    downloadBytes = download_bytes
    #: Псевдоним для :attr:`download_bytes_async`
    downloadBytesAsync = download_bytes_async
