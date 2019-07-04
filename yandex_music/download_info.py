import xml.dom.minidom as minidom

from yandex_music import YandexMusicObject


class DownloadInfo(YandexMusicObject):
    """Класс представляющий информацию о вариантах загрузки трека.

    Attributes:
        codec (:obj:`str`): Кодек аудиофайла.
        bitrate_in_kbps (:obj:`int`): Битрейт аудиофайла в кбит/с.
        gain (:obj:`bool`): Усиление TODO.
        preview (:obj:`bool`): Предварительный просмотр TODO.
        download_info_url (:obj:`str`): Ссылка на XML документ содержащий данные для загрузки трека.
        direct_link (:obj:`str`): Прямая ссылка на загрузку. Доступна после получения ссылки.
        client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
            Music.

    Args:
        codec (:obj:`str`): Кодек аудиофайла.
        bitrate_in_kbps (:obj:`int`): Битрейт аудиофайла в кбит/с.
        gain (:obj:`bool`): Усиление TODO.
        preview (:obj:`bool`): Предварительный просмотр TODO.
        download_info_url (:obj:`str`): Ссылка на XML документ содержащий данные для загрузки трека.
        client (:obj:`yandex_music.Client`, optional): Объект класса :class:`yandex_music.Client` представляющий клиент
            Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 codec,
                 bitrate_in_kbps,
                 gain,
                 preview,
                 download_info_url,
                 client=None,
                 **kwargs):
        self.codec = codec
        self.bitrate_in_kbps = bitrate_in_kbps
        self.gain = gain
        self.preview = preview
        self.download_info_url = download_info_url

        self.direct_link = None

        self.client = client

    @staticmethod
    def _get_text_node_data(elements):
        """:obj:`str`: Получение текстовой информации из узлов XML элемента."""
        for element in elements:
            nodes = element.childNodes
            for node in nodes:
                if node.nodeType == node.TEXT_NODE:
                    return node.data

    def get_direct_link(self):
        """Получение прямой ссылки на загрузку из XML ответа.

        Метод доступен только одну минуту с момента получения информации о загрузке, иначе 410 ошибка!

        Returns:
            :obj:`str`: Прямая ссылка на загрузку трека.

        """

        result = self.client.request.retrieve(self.download_info_url)

        doc = minidom.parseString(result.text)
        host = self._get_text_node_data(doc.getElementsByTagName('host'))
        path = self._get_text_node_data(doc.getElementsByTagName('path'))
        ts = self._get_text_node_data(doc.getElementsByTagName('ts'))

        self.direct_link = f'https://{host}/get-{self.codec}/randomTrash/{ts}{path}'

        return self.direct_link

    def download(self, filename):
        """Загрузка трека.

        Args:
            filename (:obj:`str`): Путь и(или) название файла вместе с расширением.
        """

        if self.direct_link is None:
            self.get_direct_link()

        self.client.request.download(self.direct_link, filename)

    @classmethod
    def de_json(cls, data, client):
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
                Music.

        Returns:
            :obj:`yandex_music.DownloadInfo`: Объект класса :class:`yandex_music.DownloadInfo`.
        """
        if not data:
            return None

        data = super(DownloadInfo, cls).de_json(data, client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data, client, get_direct_links=False):
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            get_direct_links (:obj:`bool`): Получать ли сразу прямые ссылки на загрузку.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
                Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.DownloadInfo`: Список объектов класса :class:`yandex_music.DownloadInfo`.
        """
        if not data:
            return []

        downloads_info = list()
        for download_info in data:
            downloads_info.append(cls.de_json(download_info, client))

        if get_direct_links:
            for info in downloads_info:
                info.get_direct_link()

        return downloads_info
