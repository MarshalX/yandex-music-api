from typing import TYPE_CHECKING, Optional, List

from yandex_music import YandexMusicObject
from yandex_music.exceptions import YandexMusicError
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client


@model
class MixLink(YandexMusicObject):
    """Класс, представляющий ссылку (кликабельный блок) на подборку.

    Note:
        В цветах может как оказаться HEX (`#6c65a9`), так и какой-нибудь `transparent`.

        Ссылка со схемой отличается от просто ссылки наличием `yandexmusic://` в начале.

    Attributes:
        title (:obj:`str`): Заголовок ссылки.
        url (:obj:`str`): Ссылка на подборку.
        url_scheme (:obj:`str`): Ссылка со схемой на подборку.
        text_color (:obj:`str`): Цвет текста (HEX).
        background_color (:obj:`str`): Цвет заднего фона.
        background_image_uri (:obj:`str`): Ссылка на изображение заднего фона.
        cover_white (:obj:`str`, optional): Ссылка на изображение с обложкой TODO.
        cover_uri (:obj:`str`, optional): Ссылка на изображение с обложкой.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    title: str
    url: str
    url_scheme: str
    text_color: str
    background_color: str
    background_image_uri: str
    cover_white: Optional[str] = None
    cover_uri: Optional[str] = None
    client: Optional['Client'] = None

    def __post_init__(self):
        self._id_attrs = (
            self.url,
            self.title,
            self.url_scheme,
            self.text_color,
            self.background_color,
            self.background_image_uri,
        )

    def get_cover_url(self, size: str = '200x200') -> str:
        """Возвращает URL обложки.

        Args:
            size (:obj:`str`, optional): Размер обложки.

        Returns:
            :obj:`str`: URL обложки.
        """
        return f'https://{self.cover_uri.replace("%%", size)}'

    def get_cover_white_url(self, size: str = '200x200') -> str:
        """Возвращает URL обложки white.

        Args:
            size (:obj:`str`, optional): Размер обложки.

        Returns:
            :obj:`str`: URL обложки.
        """

        if not self.cover_white:
            raise YandexMusicError('You can\'t get cover white because it\'s None.')

        return f'https://{self.cover_white.replace("%%", size)}'

    def get_background_url(self, size: str = '200x200') -> str:
        """Возвращает URL заднего фона.

        Args:
            size (:obj:`str`, optional): Размер заднего фона.

        Returns:
            :obj:`str`: URL заднего фона.
        """
        return f'https://{self.background_image_uri.replace("%%", size)}'

    def download_background_image(self, filename: str, size: str = '200x200') -> None:
        """Загрузка заднего фона.

        Args:
            filename (:obj:`str`): Путь для сохранения файла с названием и расширением.
            size (:obj:`str`, optional): Размер заднего фона.
        """
        self.client.request.download(self.get_background_url(size), filename)

    async def download_background_image_async(self, filename: str, size: str = '200x200') -> None:
        """Загрузка заднего фона.

        Args:
            filename (:obj:`str`): Путь для сохранения файла с названием и расширением.
            size (:obj:`str`, optional): Размер заднего фона.
        """
        await self.client.request.download(self.get_background_url(size), filename)

    def download_cover_white(self, filename: str, size: str = '200x200') -> None:
        """Загрузка обложки TODO.

        Args:
            filename (:obj:`str`): Путь для сохранения файла с названием и расширением.
            size (:obj:`str`, optional): Размер обложки.
        """
        self.client.request.download(self.get_cover_white_url(size), filename)

    async def download_cover_white_async(self, filename: str, size: str = '200x200') -> None:
        """Загрузка обложки TODO.

        Args:
            filename (:obj:`str`): Путь для сохранения файла с названием и расширением.
            size (:obj:`str`, optional): Размер обложки.
        """
        await self.client.request.download(self.get_cover_white_url(size), filename)

    def download_cover_uri(self, filename: str, size: str = '200x200') -> None:
        """Загрузка обложки.

        Args:
            filename (:obj:`str`): Путь для сохранения файла с названием и расширением.
            size (:obj:`str`, optional): Размер обложки.
        """
        self.client.request.download(self.get_cover_url(size), filename)

    async def download_cover_uri_async(self, filename: str, size: str = '200x200') -> None:
        """Загрузка обложки.

        Args:
            filename (:obj:`str`): Путь для сохранения файла с названием и расширением.
            size (:obj:`str`, optional): Размер обложки.
        """
        await self.client.request.download(self.get_cover_url(size), filename)

    def download_background_image_bytes(self, size: str = '200x200') -> bytes:
        """Загрузка заднего фона и возврат в виде байтов.

        Args:
            size (:obj:`str`, optional): Размер заднего фона.

        Returns:
            :obj:`bytes`: Задний фон в виде байтов.
        """
        return self.client.request.retrieve(self.get_background_url(size))

    async def download_background_image_bytes_async(self, size: str = '200x200') -> bytes:
        """Загрузка заднего фона и возврат в виде байтов.

        Args:
            size (:obj:`str`, optional): Размер заднего фона.

        Returns:
            :obj:`bytes`: Задний фон в виде байтов.
        """
        return await self.client.request.retrieve(self.get_background_url(size))

    def download_cover_white_bytes(self, size: str = '200x200') -> bytes:
        """Загрузка обложки и возврат в виде байтов TODO.

        Args:
            size (:obj:`str`, optional): Размер обложки.

        Returns:
            :obj:`bytes`: Обложка в виде байтов.
        """
        return self.client.request.retrieve(self.get_cover_white_url(size))

    async def download_cover_white_bytes_async(self, size: str = '200x200') -> bytes:
        """Загрузка обложки и возврат в виде байтов TODO.

        Args:
            size (:obj:`str`, optional): Размер обложки.

        Returns:
            :obj:`bytes`: Обложка в виде байтов.
        """
        return await self.client.request.retrieve(self.get_cover_white_url(size))

    def download_cover_uri_bytes(self, size: str = '200x200') -> bytes:
        """Загрузка обложки и возврат в виде байтов.

        Args:
            size (:obj:`str`, optional): Размер обложки.

        Returns:
            :obj:`bytes`: Обложка в виде байтов.
        """
        return self.client.request.retrieve(self.get_cover_url(size))

    async def download_cover_uri_bytes_async(self, size: str = '200x200') -> bytes:
        """Загрузка обложки и возврат в виде байтов.

        Args:
            size (:obj:`str`, optional): Размер обложки.

        Returns:
            :obj:`bytes`: Обложка в виде байтов.
        """
        return await self.client.request.retrieve(self.get_cover_url(size))

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['MixLink']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.MixLink`: Блок-ссылка на подборку.
        """
        if not data:
            return None

        data = super(MixLink, cls).de_json(data, client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data: dict, client: 'Client') -> List['MixLink']:
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.MixLink`: Блоки-ссылки на подборки.
        """
        if not data:
            return []

        mix_links = list()
        for mix_link in data:
            mix_links.append(cls.de_json(mix_link, client))

        return mix_links

    # camelCase псевдонимы

    #: Псевдоним для :attr:`get_cover_url`
    getCoverUrl = get_cover_url
    #: Псевдоним для :attr:`get_cover_white_url`
    getCoverWhiteUrl = get_cover_white_url
    #: Псевдоним для :attr:`get_background_url`
    getBackgroundUrl = get_background_url
    #: Псевдоним для :attr:`download_background_image`
    downloadBackgroundImage = download_background_image
    #: Псевдоним для :attr:`download_background_image_async`
    downloadBackgroundImageAsync = download_background_image_async
    #: Псевдоним для :attr:`download_cover_white`
    downloadCoverWhite = download_cover_white
    #: Псевдоним для :attr:`download_cover_white_async`
    downloadCoverWhiteAsync = download_cover_white_async
    #: Псевдоним для :attr:`download_cover_uri`
    downloadCoverUri = download_cover_uri
    #: Псевдоним для :attr:`download_cover_uri_async`
    downloadCoverUriAsync = download_cover_uri_async
    #: Псевдоним для :attr:`download_background_image_bytes`
    downloadBackgroundImageBytes = download_background_image_bytes
    #: Псевдоним для :attr:`download_background_image_bytes_async`
    downloadBackgroundImageBytesAsync = download_background_image_bytes_async
    #: Псевдоним для :attr:`download_cover_white_bytes`
    downloadCoverWhiteBytes = download_cover_white_bytes
    #: Псевдоним для :attr:`download_cover_white_bytes_async`
    downloadCoverWhiteBytesAsync = download_cover_white_bytes_async
    #: Псевдоним для :attr:`download_cover_uri_bytes`
    downloadCoverUriBytes = download_cover_uri_bytes
    #: Псевдоним для :attr:`download_cover_uri_bytes_async`
    downloadCoverUriBytesAsync = download_cover_uri_bytes_async
