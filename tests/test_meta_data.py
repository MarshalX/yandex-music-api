from yandex_music import MetaData


class TestMetaData:
    album = 'VK Virus Bot'
    volume = 1
    year = 2018
    number = 6
    genre = 'Techno'

    def test_expected_values(self, meta_data):
        assert meta_data.album == self.album
        assert meta_data.volume == self.volume
        assert meta_data.year == self.year
        assert meta_data.number == self.number
        assert meta_data.genre == self.genre

    def test_de_json_none(self, client):
        assert MetaData.de_json({}, client) is None

    def test_de_json_required(self, client):
        MetaData.de_json({}, client)

    def test_de_json_all(self, client):
        json_dict = {'album': self.album, 'volume': self.volume, 'year': self.year,
                     'number': self.number, 'genre': self.genre}
        meta_data = MetaData.de_json(json_dict, client)

        assert meta_data.album == self.album
        assert meta_data.volume == self.volume
        assert meta_data.year == self.year
        assert meta_data.number == self.number
        assert meta_data.genre == self.genre

    def test_equality(self):
        a = MetaData(self.album, self.volume, self.year)
        b = MetaData(self.album, 0, 2016)
        c = MetaData(self.album, self.volume, self.year)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
