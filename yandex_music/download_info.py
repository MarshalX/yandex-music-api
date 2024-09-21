import xml.dom.minidom as minidom
from hashlib import md5
from typing import TYPE_CHECKING, List, Optional

from yandex_music import JSONType, YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from xml.dom.minicompat import NodeList

    from yandex_music import ClientType

SIGN_SALT = 'XGRlBW9FXlekgbPrRHuSiA'


@model
class DownloadInfo(YandexMusicModel):
    """Класс, представляющий информацию о вариантах загрузки трека.

    Attributes:
        codec (:obj:`str`): Кодек аудиофайла.
        bitrate_in_kbps (:obj:`int`): Битрейт аудиофайла в кбит/с.
        gain (:obj:`bool`): Усиление TODO.
        preview (:obj:`bool`): Предварительный просмотр TODO.
        download_info_url (:obj:`str`): Ссылка на XML документ содержащий данные для загрузки трека.
        direct (:obj:`bool`): Прямая ли ссылка.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    codec: str
    bitrate_in_kbps: int
    gain: bool
    preview: bool
    download_info_url: str
    direct: bool
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self.direct_link = None
        self._id_attrs = (self.codec, self.bitrate_in_kbps, self.gain, self.preview, self.download_info_url)

    @staticmethod
    def _get_text_node_data(elements: 'NodeList') -> Optional[str]:
        """:obj:`str`: Получение текстовой информации из узлов XML элемента."""
        for element in elements:
            nodes = element.childNodes
            for node in nodes:
                if node.nodeType == node.TEXT_NODE:
                    return node.data

        return None

    def __build_direct_link(self, xml: bytes) -> str:
        doc = minidom.parseString(xml)  # noqa: S318
        host = self._get_text_node_data(doc.getElementsByTagName('host'))
        path = self._get_text_node_data(doc.getElementsByTagName('path'))
        ts = self._get_text_node_data(doc.getElementsByTagName('ts'))
        s = self._get_text_node_data(doc.getElementsByTagName('s'))
        sign = md5((SIGN_SALT + path[1::] + s).encode('UTF-8')).hexdigest()  # noqa: S324

        return f'https://{host}/get-mp3/{sign}/{ts}{path}'

    def get_direct_link(self) -> str:
        """Получение прямой ссылки на загрузку из XML ответа.

        Метод доступен только одну минуту с момента получения информации о загрузке, иначе 410 ошибка!

        Returns:
            :obj:`str`: Прямая ссылка на загрузку трека.

        """
        assert self.valid_client(self.client)
        result = self.client.request.retrieve(self.download_info_url)

        self.direct_link = self.__build_direct_link(result)

        return self.direct_link

    async def get_direct_link_async(self) -> str:
        """Получение прямой ссылки на загрузку из XML ответа.

        Метод доступен только одну минуту с момента получения информации о загрузке, иначе 410 ошибка!

        Returns:
            :obj:`str`: Прямая ссылка на загрузку трека.

        """
        assert self.valid_async_client(self.client)
        result = await self.client.request.retrieve(self.download_info_url)

        self.direct_link = self.__build_direct_link(result)

        return self.direct_link

    def download(self, filename: str) -> None:
        """Загрузка трека.

        Args:
            filename (:obj:`str`): Путь и(или) название файла вместе с расширением.
        """
        if self.direct_link is None:
            self.direct_link = self.get_direct_link()

        assert self.valid_client(self.client)
        self.client.request.download(self.direct_link, filename)

    async def download_async(self, filename: str) -> None:
        """Загрузка трека.

        Args:
            filename (:obj:`str`): Путь и(или) название файла вместе с расширением.
        """
        if self.direct_link is None:
            self.direct_link = await self.get_direct_link_async()

        assert self.valid_async_client(self.client)
        await self.client.request.download(self.direct_link, filename)

    def download_bytes(self) -> bytes:
        """Загрузка трека и возврат в виде байтов.

        Returns:
            :obj:`bytes`: Трек в виде байтов.
        """
        if self.direct_link is None:
            self.direct_link = self.get_direct_link()

        assert self.valid_client(self.client)
        return self.client.request.retrieve(self.direct_link)

    async def download_bytes_async(self) -> bytes:
        """Загрузка трека и возврат в виде байтов.

        Returns:
            :obj:`bytes`: Трек в виде байтов.
        """
        if self.direct_link is None:
            self.direct_link = await self.get_direct_link_async()

        assert self.valid_async_client(self.client)
        return await self.client.request.retrieve(self.direct_link)

    @classmethod
    def de_list(cls, data: JSONType, client: 'ClientType', get_direct_links: bool = False) -> List['DownloadInfo']:
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            get_direct_links (:obj:`bool`): Получать ли сразу прямые ссылки на загрузку.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.DownloadInfo`: Варианты загрузки треков.
        """
        if not cls.is_array_model_data(data):
            return []

        download_infos: List[DownloadInfo] = []
        for raw_download_info in data:
            download_info = cls.de_json(raw_download_info, client)
            if download_info:
                download_infos.append(download_info)

        if get_direct_links:
            for info in download_infos:
                info.get_direct_link()

        return download_infos

    @classmethod
    async def de_list_async(
        cls, data: 'JSONType', client: 'ClientType', get_direct_links: bool = False
    ) -> List['DownloadInfo']:
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            get_direct_links (:obj:`bool`): Получать ли сразу прямые ссылки на загрузку.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.DownloadInfo`: Варианты загрузки треков.
        """
        if not cls.is_array_model_data(data):
            return []

        download_infos: List[DownloadInfo] = []
        for raw_download_info in data:
            download_info = cls.de_json(raw_download_info, client)
            if download_info:
                download_infos.append(download_info)

        if get_direct_links:
            for info in download_infos:
                # FIXME (MarshalX): gather or something?
                await info.get_direct_link_async()

        return download_infos

    # camelCase псевдонимы

    #: Псевдоним для :attr:`get_direct_link`
    getDirectLink = get_direct_link
    #: Псевдоним для :attr:`get_direct_link_async`
    getDirectLinkAsync = get_direct_link_async
    #: Псевдоним для :attr:`download_async`
    downloadAsync = download_async
    #: Псевдоним для :attr:`download_bytes`
    downloadBytes = download_bytes
    #: Псевдоним для :attr:`download_bytes_async`
    downloadBytesAsync = download_bytes_async
