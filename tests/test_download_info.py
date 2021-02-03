import pytest

from yandex_music import DownloadInfo


@pytest.fixture(scope='class')
def download_info():
    return DownloadInfo(
        TestDownloadInfo.codec,
        TestDownloadInfo.bitrate_in_kbps,
        TestDownloadInfo.gain,
        TestDownloadInfo.preview,
        TestDownloadInfo.download_info_url,
        TestDownloadInfo.direct,
    )


class TestDownloadInfo:
    codec = 'mp3'
    bitrate_in_kbps = 192
    gain = False
    preview = False
    download_info_url = (
        'https://storage.mds.yandex.net/file-download-info/136146_d158926e.14534319.6.10994777/320'
        '?sign=8caf5ea72c946d4753f15298e4033b961c7acb1bb4db48eb5e6b59621e387d64&ts=5dc4a6f2 '
    )
    direct = False

    def test_expected_values(self, download_info):
        assert download_info.codec == self.codec
        assert download_info.bitrate_in_kbps == self.bitrate_in_kbps
        assert download_info.gain == self.gain
        assert download_info.preview == self.preview
        assert download_info.download_info_url == self.download_info_url
        assert download_info.direct == self.direct

    def test_de_json_none(self, client):
        assert DownloadInfo.de_json({}, client) is None

    def test_de_list_none(self, client):
        assert DownloadInfo.de_list({}, client) == []

    def test_de_json_required(self, client):
        json_dict = {
            'codec': self.codec,
            'bitrate_in_kbps': self.bitrate_in_kbps,
            'gain': self.gain,
            'preview': self.preview,
            'download_info_url': self.download_info_url,
            'direct': self.direct,
        }
        download_info = DownloadInfo.de_json(json_dict, client)

        assert download_info.codec == self.codec
        assert download_info.bitrate_in_kbps == self.bitrate_in_kbps
        assert download_info.gain == self.gain
        assert download_info.preview == self.preview
        assert download_info.download_info_url == self.download_info_url
        assert download_info.direct == self.direct

    def test_de_json_all(self, client):
        json_dict = {
            'codec': self.codec,
            'bitrate_in_kbps': self.bitrate_in_kbps,
            'gain': self.gain,
            'preview': self.preview,
            'download_info_url': self.download_info_url,
            'direct': self.direct,
        }
        download_info = DownloadInfo.de_json(json_dict, client)

        assert download_info.codec == self.codec
        assert download_info.bitrate_in_kbps == self.bitrate_in_kbps
        assert download_info.gain == self.gain
        assert download_info.preview == self.preview
        assert download_info.download_info_url == self.download_info_url
        assert download_info.direct == self.direct

    def test_equality(self):
        a = DownloadInfo(self.codec, self.bitrate_in_kbps, self.gain, self.preview, self.download_info_url, self.direct)
        b = DownloadInfo(self.codec, 128, self.gain, True, self.download_info_url, True)
        c = DownloadInfo(self.codec, self.bitrate_in_kbps, self.gain, self.preview, self.download_info_url, self.direct)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
