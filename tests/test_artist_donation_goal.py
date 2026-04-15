from yandex_music import ArtistDonationGoal


class TestArtistDonationGoal:
    title = 'На запись трека'

    def test_expected_value(self, artist_donation_goal):
        assert artist_donation_goal.title == self.title

    def test_de_json_none(self, client):
        assert ArtistDonationGoal.de_json({}, client) is None

    def test_de_json_all(self, client):
        json_dict = {
            'title': self.title,
        }
        obj = ArtistDonationGoal.de_json(json_dict, client)

        assert obj.title == self.title

    def test_equality(self):
        a = ArtistDonationGoal(title='На запись трека')
        b = ArtistDonationGoal(title='На клип')
        c = ArtistDonationGoal(title='На запись трека')

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
