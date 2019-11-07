import pytest

from yandex_music import DownloadInfo


@pytest.fixture(scope='class')
def download_info():
    return DownloadInfo(TestDownloadInfo.codec, TestDownloadInfo.bitrate_in_kbps, TestDownloadInfo.gain,
                        TestDownloadInfo.preview, TestDownloadInfo.download_info_url)


class TestDownloadInfo:
    codec = None
    bitrate_in_kbps = None
    gain = None
    preview = None
    download_info_url = None

    def test_expected_values(self, download_info):
        assert download_info.codec == self.codec
        assert download_info.bitrate_in_kbps == self.bitrate_in_kbps
        assert download_info.gain == self.gain
        assert download_info.preview == self.preview
        assert download_info.download_info_url == self.download_info_url

    def test_de_json_required(self, client):
        json_dict = {'codec': self.codec, 'bitrate_in_kbps': self.bitrate_in_kbps, 'gain': self.gain,
                     'preview': self.preview, 'download_info_url': self.download_info_url}
        download_info = DownloadInfo.de_json(json_dict, client)

        assert download_info.codec == self.codec
        assert download_info.bitrate_in_kbps == self.bitrate_in_kbps
        assert download_info.gain == self.gain
        assert download_info.preview == self.preview
        assert download_info.download_info_url == self.download_info_url

    def test_de_json_all(self, client):
        json_dict = {'codec': self.codec, 'bitrate_in_kbps': self.bitrate_in_kbps, 'gain': self.gain,
                     'preview': self.preview, 'download_info_url': self.download_info_url}
        download_info = DownloadInfo.de_json(json_dict, client)

        assert download_info.codec == self.codec
        assert download_info.bitrate_in_kbps == self.bitrate_in_kbps
        assert download_info.gain == self.gain
        assert download_info.preview == self.preview
        assert download_info.download_info_url == self.download_info_url

    def test_equality(self):
        pass
