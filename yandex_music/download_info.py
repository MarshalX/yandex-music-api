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

        self.client = client

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(DownloadInfo, cls).de_json(data, client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data, client):
        if not data:
            return []

        downloads_info = list()
        for download_info in data:
            downloads_info.append(cls.de_json(download_info, client))

        return downloads_info
