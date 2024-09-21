from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType


@model
class Icon(YandexMusicModel):
    """Класс, представляющий иконку.

    Attributes:
        background_color (:obj:`str`): Цвет заднего фона в HEX.
        image_url (:obj:`str`): Ссылка на изображение.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    background_color: str
    image_url: str
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.background_color, self.image_url)

    def download(self, filename: str, size: str = '200x200') -> None:
        """Загрузка иконки.

        Args:
            filename (:obj:`str`): Путь для сохранения файла с названием и расширением.
            size (:obj:`str`, optional): Размер иконки.
        """
        assert self.valid_client(self.client)
        self.client.request.download(self.get_url(size), filename)

    async def download_async(self, filename: str, size: str = '200x200') -> None:
        """Загрузка иконки.

        Args:
            filename (:obj:`str`): Путь для сохранения файла с названием и расширением.
            size (:obj:`str`, optional): Размер иконки.
        """
        assert self.valid_async_client(self.client)
        await self.client.request.download(self.get_url(size), filename)

    def download_bytes(self, size: str = '200x200') -> bytes:
        """Загрузка иконки и возврат в виде байтов.

        Args:
            size (:obj:`str`, optional): Размер иконки.

        Returns:
            :obj:`bytes`: Иконка в виде байтов.
        """
        assert self.valid_client(self.client)
        return self.client.request.retrieve(self.get_url(size))

    async def download_bytes_async(self, size: str = '200x200') -> bytes:
        """Загрузка иконки и возврат в виде байтов.

        Args:
            size (:obj:`str`, optional): Размер иконки.

        Returns:
            :obj:`bytes`: Иконка в виде байтов.
        """
        assert self.valid_async_client(self.client)
        return await self.client.request.retrieve(self.get_url(size))

    def get_url(self, size: str = '200x200') -> str:
        """Получение URL иконки.

        Args:
            size (:obj:`str`, optional): Размер иконки.
        """
        return f'https://{self.image_url.replace("%%", size)}'

    # camelCase псевдонимы

    #: Псевдоним для :attr:`download_async`
    downloadAsync = download_async
    #: Псевдоним для :attr:`download_bytes`
    downloadBytes = download_bytes
    #: Псевдоним для :attr:`download_bytes_async`
    downloadBytesAsync = download_bytes_async
    #: Псевдоним для :attr:`get_url`
    getUrl = get_url
