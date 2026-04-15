from yandex_music import ArtistSkeletonTab


class TestArtistSkeletonTab:
    id = 'web-artist-default'
    title = 'Артист'

    def test_expected_value(self, artist_skeleton_tab, artist_skeleton_block):
        assert artist_skeleton_tab.id == self.id
        assert artist_skeleton_tab.title == self.title
        assert artist_skeleton_tab.blocks == [artist_skeleton_block]

    def test_de_json_none(self, client):
        assert ArtistSkeletonTab.de_json({}, client) is None

    def test_de_json_all(self, client, artist_skeleton_block):
        json_dict = {
            'id': self.id,
            'title': self.title,
            'blocks': [artist_skeleton_block.to_dict()],
        }
        obj = ArtistSkeletonTab.de_json(json_dict, client)

        assert obj.id == self.id
        assert obj.title == self.title
        assert obj.blocks == [artist_skeleton_block]

    def test_equality(self):
        a = ArtistSkeletonTab(id='a', title='A')
        b = ArtistSkeletonTab(id='b', title='B')
        c = ArtistSkeletonTab(id='a', title='A')

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
