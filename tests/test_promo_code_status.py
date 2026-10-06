from typing import Dict

import pytest

from yandex_music import Client, JSONType, PromoCodeStatus, Status


@pytest.fixture(scope='class')
def promo_code_status(status: Status) -> PromoCodeStatus:
    return PromoCodeStatus(TestPromoCodeStatus.status, TestPromoCodeStatus.status_desc, status)


class TestPromoCodeStatus:
    status = 'user-temporary-banned'
    status_desc = 'You entered the wrong code more than 10 times. You will be able to continue in 24 hours.'

    def test_expected_values(self, promo_code_status: PromoCodeStatus, status: Status) -> None:
        assert promo_code_status.status == self.status
        assert promo_code_status.status_desc == self.status_desc
        assert promo_code_status.account_status == status

    def test_de_json_none(self, client: Client) -> None:
        assert PromoCodeStatus.de_json({}, client) is None

    def test_de_json_required(self, client: Client, status: Status) -> None:
        json_dict: Dict[str, JSONType] = {
            'status': self.status,
            'status_desc': self.status_desc,
            'account_status': status.to_dict(),
        }
        promo_code_status = PromoCodeStatus.de_json(json_dict, client)
        assert promo_code_status is not None

        assert promo_code_status.status == self.status
        assert promo_code_status.status_desc == self.status_desc
        assert promo_code_status.account_status == status

    def test_de_json_all(self, client: Client, status: Status) -> None:
        json_dict: Dict[str, JSONType] = {
            'status': self.status,
            'status_desc': self.status_desc,
            'account_status': status.to_dict(),
        }
        promo_code_status = PromoCodeStatus.de_json(json_dict, client)
        assert promo_code_status is not None

        assert promo_code_status.status == self.status
        assert promo_code_status.status_desc == self.status_desc
        assert promo_code_status.account_status == status

    def test_equality(self, status: Status) -> None:
        a = PromoCodeStatus(self.status, self.status_desc, status)
        b = PromoCodeStatus(self.status, '', status)
        c = PromoCodeStatus(self.status, self.status_desc, status)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
