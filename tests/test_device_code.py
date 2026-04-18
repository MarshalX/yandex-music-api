from yandex_music import DeviceCode


class TestDeviceCode:
    device_code = 'abcdef0123456789'
    user_code = 'ABCDEFG'
    verification_url = 'https://oauth.yandex.ru/authorize/device'
    expires_in = 300
    interval = 5

    def test_expected_values(self, device_code):
        assert device_code.device_code == self.device_code
        assert device_code.user_code == self.user_code
        assert device_code.verification_url == self.verification_url
        assert device_code.expires_in == self.expires_in
        assert device_code.interval == self.interval

    def test_de_json_none(self, client):
        assert DeviceCode.de_json({}, client) is None

    def test_de_json_required(self, client):
        json_dict = {
            'device_code': self.device_code,
            'user_code': self.user_code,
            'verification_url': self.verification_url,
            'expires_in': self.expires_in,
            'interval': self.interval,
        }
        code = DeviceCode.de_json(json_dict, client)

        assert code.device_code == self.device_code
        assert code.user_code == self.user_code
        assert code.verification_url == self.verification_url
        assert code.expires_in == self.expires_in
        assert code.interval == self.interval

    def test_equality(self):
        a = DeviceCode('a', 'U1', 'https://x', 100, 5)
        b = DeviceCode('b', 'U2', 'https://y', 200, 10)
        c = DeviceCode('a', 'U1', 'https://x', 100, 5)

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
