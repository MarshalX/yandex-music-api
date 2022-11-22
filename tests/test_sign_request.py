import datetime

from yandex_music.utils.sign_request import get_sign_request


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
