from yandex_music import Images


class TestImages:
    _208x208 = 'http://avatars.mds.yandex.net/get-music-misc/28052/metagenre-pop-x208/orig'
    _300x300 = 'http://avatars.mds.yandex.net/get-music-misc/28052/metagenre-pop-x300/orig'

    def test_expected_values(self, images):
        assert images._208x208 == self._208x208
        assert images._300x300 == self._300x300

    def test_de_json_none(self, client):
        assert Images.de_json({}, client) is None

    def test_de_json_required(self, client):
        json_dict = {}
        images = Images.de_json(json_dict, client)

    def test_de_json_all(self, client):
        json_dict = {'_208x208': self._208x208, '_300x300': self._300x300}
        images = Images.de_json(json_dict, client)

        assert images._208x208 == self._208x208
        assert images._300x300 == self._300x300

    def test_equality(self):
        a = Images(self._208x208, self._300x300)
        b = Images(self._208x208, self._300x300)

        assert a == b
