from yandex_music import Account


class TestAccount:
    now = '2019-11-07T21:49:54+00:00'
    region = 149
    service_available = True
    uid = 1130000002804451
    login = 'Ilya@marshal.by'
    full_name = 'Семёнов Илья'
    second_name = 'Семёнов'
    first_name = 'Илья'
    display_name = 'Il`ya (Marshal)'
    hosted_user = False
    birthday = '1999-08-10'
    registered_at = '2018-06-10T09:34:22+00:00'
    has_info_for_app_metrica = False

    def test_expected_values(self, account, passport_phone):
        assert account.now == self.now
        assert account.region == self.region
        assert account.service_available == self.service_available
        assert account.uid == self.uid
        assert account.login == self.login
        assert account.full_name == self.full_name
        assert account.second_name == self.second_name
        assert account.first_name == self.first_name
        assert account.display_name == self.display_name
        assert account.hosted_user == self.hosted_user
        assert account.birthday == self.birthday
        assert account.passport_phones == [passport_phone]
        assert account.registered_at == self.registered_at
        assert account.has_info_for_app_metrica == self.has_info_for_app_metrica

    def test_de_json_none(self, client):
        assert Account.de_json({}, client) is None

    def test_de_json_required(self, client):
        json_dict = {'now': self.now, 'service_available': self.service_available}
        account = Account.de_json(json_dict, client)

        assert account.now == self.now
        assert account.service_available == self.service_available

    def test_de_json_all(self, client, passport_phone):
        json_dict = {
            'now': self.now,
            'region': self.region,
            'service_available': self.service_available,
            'uid': self.uid,
            'login': self.login,
            'full_name': self.full_name,
            'second_name': self.second_name,
            'first_name': self.first_name,
            'display_name': self.display_name,
            'hosted_user': self.hosted_user,
            'birthday': self.birthday,
            'passport_phones': [passport_phone.to_dict()],
            'registered_at': self.registered_at,
            'has_info_for_app_metrica': self.has_info_for_app_metrica,
        }
        account = Account.de_json(json_dict, client)

        assert account.now == self.now
        assert account.region == self.region
        assert account.service_available == self.service_available
        assert account.uid == self.uid
        assert account.login == self.login
        assert account.full_name == self.full_name
        assert account.second_name == self.second_name
        assert account.first_name == self.first_name
        assert account.display_name == self.display_name
        assert account.hosted_user == self.hosted_user
        assert account.birthday == self.birthday
        assert account.passport_phones == [passport_phone]
        assert account.registered_at == self.registered_at
        assert account.has_info_for_app_metrica == self.has_info_for_app_metrica

    def test_equality(self, user):
        a = Account(self.now, self.service_available)

        assert a != user
        assert hash(a) != hash(user)
        assert a is not user
