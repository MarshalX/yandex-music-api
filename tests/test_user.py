from yandex_music import User


class TestUser:
    uid = 503646255
    login = 'yamusic-daily'
    name = 'yamusic-daily'
    display_name = 'Ilya (Marshal)'
    full_name = 'Илья'
    sex = 'unknown'
    verified = False
    regions = ['RUSSIA_PREMIUM', 'RUSSIA']

    def test_expected_values(self, user):
        assert user.uid == self.uid
        assert user.login == self.login
        assert user.name == self.name
        assert user.display_name == self.display_name
        assert user.full_name == self.full_name
        assert user.sex == self.sex
        assert user.verified == self.verified
        assert user.regions == self.regions

    def test_de_json_none(self, client):
        assert User.de_json({}, client) is None

    def test_de_list_none(self, client):
        assert User.de_list({}, client) == []

    def test_de_json_required(self, client):
        json_dict = {'uid': self.uid, 'login': self.login}
        user = User.de_json(json_dict, client)

        assert user.uid == self.uid
        assert user.login == self.login

    def test_de_json_all(self, client):
        json_dict = {
            'uid': self.uid,
            'login': self.login,
            'name': self.name,
            'sex': self.sex,
            'verified': self.verified,
            'display_name': self.display_name,
            'full_name': self.full_name,
            'regions': self.regions,
        }
        user = User.de_json(json_dict, client)

        assert user.uid == self.uid
        assert user.login == self.login
        assert user.name == self.name
        assert user.display_name == self.display_name
        assert user.full_name == self.full_name
        assert user.sex == self.sex
        assert user.verified == self.verified
        assert user.regions == self.regions

    def test_equality(self):
        a = User(self.uid, self.login)
        b = User(1, self.login)
        c = User(self.uid, self.login)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
