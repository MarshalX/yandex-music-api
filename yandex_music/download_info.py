import xml.dom.minidom as minidom

from yandex_music import YandexMusicObject


class DownloadInfo(YandexMusicObject):
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
        for element in elements:
            nodes = element.childNodes
            for node in nodes:
                if node.nodeType == node.TEXT_NODE:
                    return node.data

    def get_direct_link(self):
        # Available within one minute after receiving download_info, otherwise 410!
        result = self.client._request.retrieve(self.download_info_url)

        doc = minidom.parseString(result.text)
        host = self._get_text_node_data(doc.getElementsByTagName('host'))
        path = self._get_text_node_data(doc.getElementsByTagName('path'))
        ts = self._get_text_node_data(doc.getElementsByTagName('ts'))

        self.direct_link = f'https://{host}/get-{self.codec}/randomTrash/{ts}{path}'

        return self.direct_link

    def download(self, filename):
        if self.direct_link is None:
            self.get_direct_link()

        self.client._request.download(self.direct_link, filename)

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(DownloadInfo, cls).de_json(data, client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data, client, get_direct_links=False):
        if not data:
            return []

        downloads_info = list()
        for download_info in data:
            downloads_info.append(cls.de_json(download_info, client))

        if get_direct_links:
            for info in downloads_info:
                info.get_direct_link()

        return downloads_info
