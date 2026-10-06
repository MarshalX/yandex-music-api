from typing import Dict

from yandex_music import Client, Images, JSONType


class TestImages:
    _208x208 = 'http://avatars.mds.yandex.net/get-music-misc/28052/metagenre-pop-x208/orig'
    _300x300 = 'http://avatars.mds.yandex.net/get-music-misc/28052/metagenre-pop-x300/orig'

    def test_expected_values(self, images: Images) -> None:
        assert images._208x208 == self._208x208
        assert images._300x300 == self._300x300

    def test_de_json_none(self, client: Client) -> None:
        assert Images.de_json({}, client) is None

    def test_de_json_required(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {}
        _ = Images.de_json(json_dict, client)

    def test_de_json_all(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {'_208x208': self._208x208, '_300x300': self._300x300}
        images = Images.de_json(json_dict, client)
        assert images is not None

        assert images._208x208 == self._208x208
        assert images._300x300 == self._300x300

    def test_equality(self) -> None:
        a = Images(self._208x208, self._300x300)
        b = Images(self._208x208, self._300x300)

        assert a == b
