from yandex_music import SkeletonViewAllAction


class TestSkeletonViewAllAction:
    deeplink = 'yandexmusic://artist/12345/all/albums'
    weblink = '/artist/12345/albums'

    def test_expected_value(self, skeleton_view_all_action):
        assert skeleton_view_all_action.deeplink == self.deeplink
        assert skeleton_view_all_action.weblink == self.weblink

    def test_de_json_none(self, client):
        assert SkeletonViewAllAction.de_json({}, client) is None

    def test_de_json_all(self, client):
        json_dict = {
            'deeplink': self.deeplink,
            'weblink': self.weblink,
        }
        obj = SkeletonViewAllAction.de_json(json_dict, client)

        assert obj.deeplink == self.deeplink
        assert obj.weblink == self.weblink

    def test_equality(self):
        a = SkeletonViewAllAction(deeplink=self.deeplink, weblink=self.weblink)
        b = SkeletonViewAllAction(deeplink='other', weblink='other')
        c = SkeletonViewAllAction(deeplink=self.deeplink, weblink=self.weblink)

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
