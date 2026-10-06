import base64
import datetime
import hashlib
import hmac

from yandex_music.utils.sign_request import get_file_info_sign, get_sign_request


class TestSignRequest:
    timestamp = 1668687184
    track_id = 4784420
    key = 'SUPER_SECRET_KEY'

    sign_value = 'vssEEweZhgv2Aud0rdH9maOXUC03ZkZ/hlo6bSRN8Qg='

    def test_sign_request(self, monkeypatch):
        class FakeDatetime(datetime.datetime):
            @classmethod
            def now(cls):
                return datetime.datetime.fromtimestamp(self.timestamp)

        monkeypatch.setattr('datetime.datetime', FakeDatetime)
        sign = get_sign_request(self.track_id, self.key)

        assert sign.timestamp == self.timestamp
        assert sign.value == self.sign_value


class TestFileInfoSign:
    timestamp = 1668687184
    track_id = '4784420:100500'
    quality = 'lossless'
    codecs = ['flac', 'aac', 'mp3']
    transport = 'encraw'
    key = 'SUPER_SECRET_KEY'

    def test_file_info_sign(self, monkeypatch):
        class FakeDatetime(datetime.datetime):
            @classmethod
            def now(cls):
                return datetime.datetime.fromtimestamp(self.timestamp)

        monkeypatch.setattr('datetime.datetime', FakeDatetime)
        sign = get_file_info_sign(self.track_id, self.quality, self.codecs, self.transport, self.key)

        message = f'{self.timestamp}{self.track_id}losslessflacaacmp3encraw'.encode()
        expected = base64.b64encode(hmac.new(self.key.encode(), message, hashlib.sha256).digest()).decode()[:-1]

        assert sign.timestamp == self.timestamp
        assert sign.value == expected
        assert not sign.value.endswith('=')
