from yandex_music import AutoRenewable


class TestAutoRenewable:
    expires = None
    vendor = None
    vendor_help_url = None
    product_id = None
    finished = None
    order_id = None

    def test_expected_values(self, auto_renewable, product):
        assert auto_renewable.expires == self.expires
        assert auto_renewable.vendor == self.vendor
        assert auto_renewable.vendor_help_url == self.vendor_help_url
        assert auto_renewable.product_id == self.product_id
        assert auto_renewable.product == product
        assert auto_renewable.finished == self.finished
        assert auto_renewable.order_id == self.order_id

    def test_de_json_required(self, client, product):
        json_dict = {'expires': self.expires, 'vendor': self.vendor, 'vendor_help_url': self.vendor_help_url,
                     'product_id': self.product_id, 'product': product, 'finished': self.finished}
        auto_renewable = AutoRenewable.de_json(json_dict, client)

        assert auto_renewable.expires == self.expires
        assert auto_renewable.vendor == self.vendor
        assert auto_renewable.vendor_help_url == self.vendor_help_url
        assert auto_renewable.product_id == self.product_id
        assert auto_renewable.product == product
        assert auto_renewable.finished == self.finished

    def test_de_json_all(self, client, product):
        json_dict = {'expires': self.expires, 'vendor': self.vendor, 'vendor_help_url': self.vendor_help_url,
                     'product_id': self.product_id, 'product': product, 'finished': self.finished,
                     'order_id': self.order_id}
        auto_renewable = AutoRenewable.de_json(json_dict, client)

        assert auto_renewable.expires == self.expires
        assert auto_renewable.vendor == self.vendor
        assert auto_renewable.vendor_help_url == self.vendor_help_url
        assert auto_renewable.product_id == self.product_id
        assert auto_renewable.product == product
        assert auto_renewable.finished == self.finished
        assert auto_renewable.order_id == self.order_id

    def test_equality(self):
        pass
