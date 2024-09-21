from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType


@model
class Images(YandexMusicModel):
    """Класс, представляющий изображение жанра.

    Attributes:
        _208x208 (:obj:`str`, optional): Ссылка на изображение размером 208 на 208.
        _300x300 (:obj:`str`, optional): Ссылка на изображение размером 300 на 300.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    _208x208: Optional[str] = None
    _300x300: Optional[str] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self._208x208, self._300x300)

    def download_208x208(self, filename: str) -> None:
        """Загрузка изображения 208x208.

        Args:
            filename (:obj:`str`): Путь для сохранения файла с названием и расширением.
        """
        assert isinstance(self._208x208, str)
        assert self.valid_client(self.client)
        self.client.request.download(self._208x208, filename)

    async def download_208x208_async(self, filename: str) -> None:
        """Загрузка изображения 208x208.

        Args:
            filename (:obj:`str`): Путь для сохранения файла с названием и расширением.
        """
        assert isinstance(self._208x208, str)
        assert self.valid_async_client(self.client)
        await self.client.request.download(self._208x208, filename)

    def download_300x300(self, filename: str) -> None:
        """Загрузка изображения 300x300.

        Args:
            filename (:obj:`str`): Путь для сохранения файла с названием и расширением.
        """
        assert isinstance(self._300x300, str)
        assert self.valid_client(self.client)
        self.client.request.download(self._300x300, filename)

    async def download_300x300_async(self, filename: str) -> None:
        """Загрузка изображения 300x300.

        Args:
            filename (:obj:`str`): Путь для сохранения файла с названием и расширением.
        """
        assert isinstance(self._300x300, str)
        assert self.valid_async_client(self.client)
        await self.client.request.download(self._300x300, filename)

    def download_208x208_bytes(self) -> bytes:
        """Загрузка изображения 208x208 и возврат в виде байтов.

        Returns:
            :obj:`bytes`: Изображение в виде байтов.
        """
        assert isinstance(self._208x208, str)
        assert self.valid_client(self.client)
        return self.client.request.retrieve(self._208x208)

    async def download_208x208_bytes_async(self) -> bytes:
        """Загрузка изображения 208x208 и возврат в виде байтов.

        Returns:
            :obj:`bytes`: Изображение в виде байтов.
        """
        assert isinstance(self._208x208, str)
        assert self.valid_async_client(self.client)
        return await self.client.request.retrieve(self._208x208)

    def download_300x300_bytes(self) -> bytes:
        """Загрузка изображения 300x300 и возврат в виде байтов.

        Returns:
            :obj:`bytes`: Изображение в виде байтов.
        """
        assert isinstance(self._300x300, str)
        assert self.valid_client(self.client)
        return self.client.request.retrieve(self._300x300)

    async def download_300x300_bytes_async(self) -> bytes:
        """Загрузка изображения 300x300 и возврат в виде байтов.

        Returns:
            :obj:`bytes`: Изображение в виде байтов.
        """
        assert isinstance(self._300x300, str)
        assert self.valid_async_client(self.client)
        return await self.client.request.retrieve(self._300x300)

    # camelCase псевдонимы

    #: Псевдоним для :attr:`download_208x208`
    download208X208 = download_208x208
    #: Псевдоним для :attr:`download_300x300`
    download300X300 = download_300x300
    #: Псевдоним для :attr:`download_208x208_bytes`
    download208X208Bytes = download_208x208_bytes
    #: Псевдоним для :attr:`download_300x300_bytes`
    download300X300Bytes = download_300x300_bytes
