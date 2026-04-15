from yandex_music import ArtistSkeletonViewAllAction


class TestArtistSkeletonViewAllAction:
    deeplink = 'yandexmusic://artist/12345/all/albums'
    weblink = '/artist/12345/albums'

    def test_expected_value(self, artist_skeleton_view_all_action):
        assert artist_skeleton_view_all_action.deeplink == self.deeplink
        assert artist_skeleton_view_all_action.weblink == self.weblink

    def test_de_json_none(self, client):
        assert ArtistSkeletonViewAllAction.de_json({}, client) is None

    def test_de_json_all(self, client):
        json_dict = {
            'deeplink': self.deeplink,
            'weblink': self.weblink,
        }
        obj = ArtistSkeletonViewAllAction.de_json(json_dict, client)

        assert obj.deeplink == self.deeplink
        assert obj.weblink == self.weblink

    def test_equality(self):
        a = ArtistSkeletonViewAllAction(deeplink=self.deeplink, weblink=self.weblink)
        b = ArtistSkeletonViewAllAction(deeplink='other', weblink='other')
        c = ArtistSkeletonViewAllAction(deeplink=self.deeplink, weblink=self.weblink)

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
