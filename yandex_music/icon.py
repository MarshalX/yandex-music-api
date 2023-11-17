from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicObject
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client


@model
class Icon(YandexMusicObject):
    """Класс, представляющий иконку.

    Attributes:
        background_color (:obj:`str`): Цвет заднего фона в HEX.
        image_url (:obj:`str`): Ссылка на изображение.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    background_color: str
    image_url: str
    client: Optional['Client'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.background_color, self.image_url)

    def download(self, filename: str, size: str = '200x200') -> None:
        """Загрузка иконки.

        Args:
            filename (:obj:`str`): Путь для сохранения файла с названием и расширением.
            size (:obj:`str`, optional): Размер иконки.
        """
        self.client.request.download(self.get_url(size), filename)

    async def download_async(self, filename: str, size: str = '200x200') -> None:
        """Загрузка иконки.

        Args:
            filename (:obj:`str`): Путь для сохранения файла с названием и расширением.
            size (:obj:`str`, optional): Размер иконки.
        """
        await self.client.request.download(self.get_url(size), filename)

    def download_bytes(self, size: str = '200x200') -> bytes:
        """Загрузка иконки и возврат в виде байтов.

        Args:
            size (:obj:`str`, optional): Размер иконки.

        Returns:
            :obj:`bytes`: Иконка в виде байтов.
        """
        return self.client.request.retrieve(self.get_url(size))

    async def download_bytes_async(self, size: str = '200x200') -> bytes:
        """Загрузка иконки и возврат в виде байтов.

        Args:
            size (:obj:`str`, optional): Размер иконки.

        Returns:
            :obj:`bytes`: Иконка в виде байтов.
        """
        return await self.client.request.retrieve(self.get_url(size))

    def get_url(self, size: str = '200x200') -> str:
        """Получение URL иконки.

        Args:
            size (:obj:`str`, optional): Размер иконки.
        """
        return f'https://{self.image_url.replace("%%", size)}'

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Icon']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Icon`: Иконка.
        """
        if not cls.is_valid_model_data(data):
            return None

        data = super(Icon, cls).de_json(data, client)

        return cls(client=client, **data)

    # camelCase псевдонимы

    #: Псевдоним для :attr:`download_async`
    downloadAsync = download_async
    #: Псевдоним для :attr:`download_bytes`
    downloadBytes = download_bytes
    #: Псевдоним для :attr:`download_bytes_async`
    downloadBytesAsync = download_bytes_async
    #: Псевдоним для :attr:`get_url`
    getUrl = get_url
