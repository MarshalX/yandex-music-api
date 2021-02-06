from yandex_music import AutoRenewable


class TestAutoRenewable:
    expires = '2019-11-30T23:59:59+03:00'
    vendor = 'Yandex'
    vendor_help_url = 'https://www.yandex.ru/support/music-app/subscription.xml'
    product_id = 'ru.yandex.mobile.music.1month.autorenewable.native.web.notrial.restricted.cache.99'
    finished = False
    order_id = 39385401

    def test_expected_values(self, auto_renewable, product, user):
        assert auto_renewable.expires == self.expires
        assert auto_renewable.vendor == self.vendor
        assert auto_renewable.vendor_help_url == self.vendor_help_url
        assert auto_renewable.product_id == self.product_id
        assert auto_renewable.product == product
        assert auto_renewable.finished == self.finished
        assert auto_renewable.master_info == user
        assert auto_renewable.order_id == self.order_id

    def test_de_json_none(self, client):
        assert AutoRenewable.de_json({}, client) is None

    def test_de_list_none(self, client):
        assert AutoRenewable.de_list({}, client) == []

    def test_de_json_required(self, client, product):
        json_dict = {
            'expires': self.expires,
            'vendor': self.vendor,
            'vendor_help_url': self.vendor_help_url,
            'product': product.to_dict(),
            'finished': self.finished,
        }
        auto_renewable = AutoRenewable.de_json(json_dict, client)

        assert auto_renewable.expires == self.expires
        assert auto_renewable.vendor == self.vendor
        assert auto_renewable.vendor_help_url == self.vendor_help_url
        assert auto_renewable.product == product
        assert auto_renewable.finished == self.finished

    def test_de_json_all(self, client, product, user):
        json_dict = {
            'expires': self.expires,
            'vendor': self.vendor,
            'vendor_help_url': self.vendor_help_url,
            'product_id': self.product_id,
            'product': product.to_dict(),
            'finished': self.finished,
            'order_id': self.order_id,
            'master_info': user.to_dict(),
        }
        auto_renewable = AutoRenewable.de_json(json_dict, client)

        assert auto_renewable.expires == self.expires
        assert auto_renewable.vendor == self.vendor
        assert auto_renewable.vendor_help_url == self.vendor_help_url
        assert auto_renewable.product_id == self.product_id
        assert auto_renewable.product == product
        assert auto_renewable.finished == self.finished
        assert auto_renewable.master_info == user
        assert auto_renewable.order_id == self.order_id

    def test_equality(self, product):
        a = AutoRenewable(self.expires, self.vendor, self.vendor_help_url, product, self.finished)
        b = AutoRenewable(self.expires, '', self.vendor_help_url, None, self.finished)
        c = AutoRenewable(self.expires, self.vendor, self.vendor_help_url, product, self.finished)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
