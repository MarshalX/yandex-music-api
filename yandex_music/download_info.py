from typing import TYPE_CHECKING, Optional, List

from hashlib import md5
import xml.dom.minidom as minidom

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client
    from xml.dom.minicompat import NodeList


class DownloadInfo(YandexMusicObject):
    """Класс, представляющий информацию о вариантах загрузки трека.

    Attributes:
        codec (:obj:`str`): Кодек аудиофайла.
        bitrate_in_kbps (:obj:`int`): Битрейт аудиофайла в кбит/с.
        gain (:obj:`bool`): Усиление TODO.
        preview (:obj:`bool`): Предварительный просмотр TODO.
        download_info_url (:obj:`str`): Ссылка на XML документ содержащий данные для загрузки трека.
        direct (:obj:`bool`): Прямая ли ссылка.
        direct_link (:obj:`str`): Прямая ссылка на загрузку. Доступна после получения ссылки.
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.

    Args:
        codec (:obj:`str`): Кодек аудиофайла.
        bitrate_in_kbps (:obj:`int`): Битрейт аудиофайла в кбит/с.
        gain (:obj:`bool`): Усиление TODO.
        preview (:obj:`bool`): Предварительный просмотр TODO.
        download_info_url (:obj:`str`): Ссылка на XML документ содержащий данные для загрузки трека.
        direct (:obj:`bool`): Прямая ли ссылка.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 codec: str,
                 bitrate_in_kbps: int,
                 gain: bool,
                 preview: bool,
                 download_info_url: str,
                 direct: bool,
                 client: Optional['Client'] = None,
                 **kwargs):
        self.codec = codec
        self.bitrate_in_kbps = bitrate_in_kbps
        self.gain = gain
        self.preview = preview
        self.download_info_url = download_info_url
        self.direct = direct

        self.direct_link = None

        self.client = client
        self._id_attrs = (self.codec, self.bitrate_in_kbps, self.gain, self.preview, self.download_info_url)

        super().handle_unknown_kwargs(self, **kwargs)

    @staticmethod
    def _get_text_node_data(elements: 'NodeList') -> str:
        """:obj:`str`: Получение текстовой информации из узлов XML элемента."""
        for element in elements:
            nodes = element.childNodes
            for node in nodes:
                if node.nodeType == node.TEXT_NODE:
                    return node.data

    async def get_direct_link(self) -> str:
        """Получение прямой ссылки на загрузку из XML ответа.

        Метод доступен только одну минуту с момента получения информации о загрузке, иначе 410 ошибка!

        Returns:
            :obj:`str`: Прямая ссылка на загрузку трека.

        """
        result = await self.client.request.retrieve(self.download_info_url)

        doc = minidom.parseString(result.text)
        host = self._get_text_node_data(doc.getElementsByTagName('host'))
        path = self._get_text_node_data(doc.getElementsByTagName('path'))
        ts = self._get_text_node_data(doc.getElementsByTagName('ts'))
        s = self._get_text_node_data(doc.getElementsByTagName('s'))
        sign = md5(('XGRlBW9FXlekgbPrRHuSiA' + path[1::] + s).encode('utf-8')).hexdigest()

        self.direct_link = f'https://{host}/get-mp3/{sign}/{ts}{path}'

        return self.direct_link

    async def download(self, filename: str) -> None:
        """Загрузка трека.

        Args:
            filename (:obj:`str`): Путь и(или) название файла вместе с расширением.
        """
        if self.direct_link is None:
            await self.get_direct_link()

        self.client.request.download(self.direct_link, filename)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['DownloadInfo']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.DownloadInfo`: Варианты загрузки треков.
        """
        if not data:
            return None

        data = super(DownloadInfo, cls).de_json(data, client)

        return cls(client=client, **data)

    @classmethod
    async def de_list(cls, data: dict, client: 'Client', get_direct_links: bool = False) -> List['DownloadInfo']:
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            get_direct_links (:obj:`bool`): Получать ли сразу прямые ссылки на загрузку.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.DownloadInfo`: Варианты загрузки треков.
        """
        if not data:
            return []

        downloads_info = list()
        for download_info in data:
            await downloads_info.append(cls.de_json(download_info, client))

        if get_direct_links:
            for info in downloads_info:
                info.get_direct_link()

        return downloads_info

    # camelCase псевдонимы

    #: Псевдоним для :attr:`get_direct_link`
    getDirectLink = get_direct_link
