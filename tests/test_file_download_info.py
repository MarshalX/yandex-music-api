import sys

import pytest

from yandex_music import FileDownloadInfo
from yandex_music.exceptions import YandexMusicError


class TestFileDownloadInfo:
    track_id = '12345:100500'
    quality = 'lossless'
    codec = 'flac-mp4'
    bitrate = 0
    transport = 'encraw'
    url = 'https://strm.example.com/music-v2/crypt/ysign1=fake/0/12345/fake.12345/flac-mp4'
    urls = [url, 'https://strm2.example.com/music-v2/crypt/ysign1=fake/0/12345/fake.12345/flac-mp4']
    real_id = '12345'
    gain = False
    key = '000102030405060708090a0b0c0d0e0f'

    def test_expected_values(self, file_download_info):
        assert file_download_info.track_id == self.track_id
        assert file_download_info.quality == self.quality
        assert file_download_info.codec == self.codec
        assert file_download_info.bitrate == self.bitrate
        assert file_download_info.transport == self.transport
        assert file_download_info.url == self.url
        assert file_download_info.urls == self.urls
        assert file_download_info.real_id == self.real_id
        assert file_download_info.gain == self.gain
        assert file_download_info.key == self.key

    def test_de_json_none(self, client):
        assert FileDownloadInfo.de_json({}, client) is None

    def test_de_json_required(self, client):
        json_dict = {
            'trackId': self.track_id,
            'quality': self.quality,
            'codec': self.codec,
            'bitrate': self.bitrate,
            'transport': self.transport,
            'url': self.url,
            'urls': self.urls,
        }
        file_download_info = FileDownloadInfo.de_json(json_dict, client)

        assert file_download_info.track_id == self.track_id
        assert file_download_info.codec == self.codec
        assert file_download_info.urls == self.urls
        assert file_download_info.key is None

    def test_de_json_all(self, client):
        json_dict = {
            'trackId': self.track_id,
            'quality': self.quality,
            'codec': self.codec,
            'bitrate': self.bitrate,
            'transport': self.transport,
            'url': self.url,
            'urls': self.urls,
            'realId': self.real_id,
            'gain': self.gain,
            'key': self.key,
        }
        file_download_info = FileDownloadInfo.de_json(json_dict, client)

        assert file_download_info.track_id == self.track_id
        assert file_download_info.quality == self.quality
        assert file_download_info.codec == self.codec
        assert file_download_info.bitrate == self.bitrate
        assert file_download_info.transport == self.transport
        assert file_download_info.url == self.url
        assert file_download_info.urls == self.urls
        assert file_download_info.real_id == self.real_id
        assert file_download_info.gain == self.gain
        assert file_download_info.key == self.key

    def test_decrypt_encraw(self, file_download_info):
        cryptography = pytest.importorskip('cryptography.hazmat.primitives.ciphers')

        plain = b'fLaC fake audio payload' * 10
        cipher = cryptography.Cipher(
            cryptography.algorithms.AES(bytes.fromhex(self.key)), cryptography.modes.CTR(bytes(16))
        ).encryptor()
        encrypted = cipher.update(plain) + cipher.finalize()

        assert encrypted != plain
        assert file_download_info._decrypt(encrypted) == plain

    def test_decrypt_without_cryptography(self, file_download_info, monkeypatch):
        monkeypatch.setitem(sys.modules, 'cryptography.hazmat.primitives.ciphers', None)

        with pytest.raises(YandexMusicError, match=r'yandex-music\[crypto\]'):
            file_download_info._decrypt(b'payload')

    def test_decrypt_raw(self):
        info = FileDownloadInfo(
            self.track_id, self.quality, self.codec, self.bitrate, 'raw', self.url, self.urls, key=self.key
        )

        assert info._decrypt(b'payload') == b'payload'

    def test_equality(self):
        a = FileDownloadInfo(self.track_id, self.quality, self.codec, self.bitrate, self.transport, self.url, self.urls)
        b = FileDownloadInfo(self.track_id, 'hq', 'aac-mp4', 256, self.transport, self.url, self.urls)
        c = FileDownloadInfo(self.track_id, self.quality, self.codec, self.bitrate, self.transport, self.url, self.urls)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
