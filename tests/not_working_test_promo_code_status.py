import pytest

from yandex_music import PromoCodeStatus


@pytest.fixture(scope='class')
def promo_code_status(account_status):
    return PromoCodeStatus(TestPromoCodeStatus.status, TestPromoCodeStatus.status_desc, account_status)


class TestPromoCodeStatus:
    status = None
    status_desc = None

    def test_expected_values(self, promo_code_status, account_status):
        assert promo_code_status.status == self.status
        assert promo_code_status.status_desc == self.status_desc
        assert promo_code_status.account_status == account_status

    def test_de_json_required(self, client, account_status):
        json_dict = {'status': self.status, 'status_desc': self.status_desc, 'account_status': account_status}
        promo_code_status = PromoCodeStatus.de_json(json_dict, client)

        assert promo_code_status.status == self.status
        assert promo_code_status.status_desc == self.status_desc
        assert promo_code_status.account_status == account_status

    def test_de_json_all(self, client, account_status):
        json_dict = {'status': self.status, 'status_desc': self.status_desc, 'account_status': account_status}
        promo_code_status = PromoCodeStatus.de_json(json_dict, client)

        assert promo_code_status.status == self.status
        assert promo_code_status.status_desc == self.status_desc
        assert promo_code_status.account_status == account_status

    def test_equality(self):
        pass
