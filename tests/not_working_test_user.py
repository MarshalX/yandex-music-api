import pytest

from yandex_music import User


@pytest.fixture(scope='class')
def user():
    return User(TestUser.uid, TestUser.login, TestUser.name, TestUser.sex, TestUser.verified)


class TestUser:
    uid = None
    login = None
    name = None
    sex = None
    verified = None

    def test_expected_values(self, user):
        assert user.uid == self.uid
        assert user.login == self.login
        assert user.name == self.name
        assert user.sex == self.sex
        assert user.verified == self.verified

    def test_de_json_required(self, client):
        json_dict = {'uid': self.uid, 'login': self.login, 'name': self.name, 'sex': self.sex,
                     'verified': self.verified}
        user = User.de_json(json_dict, client)

        assert user.uid == self.uid
        assert user.login == self.login
        assert user.name == self.name
        assert user.sex == self.sex
        assert user.verified == self.verified

    def test_de_json_all(self, client):
        json_dict = {'uid': self.uid, 'login': self.login, 'name': self.name, 'sex': self.sex,
                     'verified': self.verified}
        user = User.de_json(json_dict, client)

        assert user.uid == self.uid
        assert user.login == self.login
        assert user.name == self.name
        assert user.sex == self.sex
        assert user.verified == self.verified

    def test_equality(self):
        pass
