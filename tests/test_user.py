from yandex_music import User


class TestUser:
    uid = 503646255
    login = 'yamusic-daily'
    name = 'yamusic-daily'
    sex = 'unknown'
    verified = False

    def test_expected_values(self, user):
        assert user.uid == self.uid
        assert user.login == self.login
        assert user.name == self.name
        assert user.sex == self.sex
        assert user.verified == self.verified

    def test_de_json_none(self, client):
        assert User.de_json({}, client) is None

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
        a = User(self.uid, self.login, self.name, self.sex, self.verified)
        b = User(1, self.login, self.name, self.sex, self.verified)
        c = User(self.uid, self.login, '', self.sex, self.verified)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
