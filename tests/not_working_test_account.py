from yandex_music import Account


class TestAccount:
    now = None
    region = None
    service_available = None
    uid = None
    login = None
    full_name = None
    second_name = None
    first_name = None
    display_name = None
    hosted_user = None
    birthday = None
    registered_at = None
    has_info_for_app_metrica = None

    def test_expected_values(self, account, passport_phones):
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
        assert account.passport_phones == passport_phones
        assert account.registered_at == self.registered_at
        assert account.has_info_for_app_metrica == self.has_info_for_app_metrica

    def test_de_json_required(self, client):
        json_dict = {'now': self.now, 'region': self.region, 'service_available': self.service_available}
        account = Account.de_json(json_dict, client)

        assert account.now == self.now
        assert account.region == self.region
        assert account.service_available == self.service_available

    def test_de_json_all(self, client, passport_phones):
        json_dict = {'now': self.now, 'region': self.region, 'service_available': self.service_available,
                     'uid': self.uid, 'login': self.login, 'full_name': self.full_name, 'second_name': self.second_name,
                     'first_name': self.first_name, 'display_name': self.display_name, 'hosted_user': self.hosted_user,
                     'birthday': self.birthday, 'passport_phones': passport_phones, 'registered_at': self.registered_at,
                     'has_info_for_app_metrica': self.has_info_for_app_metrica}
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
        assert account.passport_phones == passport_phones
        assert account.registered_at == self.registered_at
        assert account.has_info_for_app_metrica == self.has_info_for_app_metrica

    def test_equality(self):
        pass
