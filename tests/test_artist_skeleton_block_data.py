from yandex_music import ArtistSkeletonBlockData


class TestArtistSkeletonBlockData:
    selected_tab_index = 0
    title = 'Популярные треки'
    show_policy = 'SHOW_AND_LOAD'

    def test_expected_value(self, artist_skeleton_block_data, artist_skeleton_source, artist_skeleton_view_all_action):
        assert artist_skeleton_block_data.source == artist_skeleton_source
        assert artist_skeleton_block_data.title == self.title
        assert artist_skeleton_block_data.show_policy == self.show_policy
        assert artist_skeleton_block_data.view_all_action == artist_skeleton_view_all_action

    def test_de_json_none(self, client):
        assert ArtistSkeletonBlockData.de_json({}, client) is None

    def test_de_json_all(self, client, artist_skeleton_source, artist_skeleton_view_all_action):
        json_dict = {
            'source': artist_skeleton_source.to_dict(),
            'title': self.title,
            'showPolicy': self.show_policy,
            'viewAllAction': artist_skeleton_view_all_action.to_dict(),
        }
        obj = ArtistSkeletonBlockData.de_json(json_dict, client)

        assert obj.source == artist_skeleton_source
        assert obj.title == self.title
        assert obj.show_policy == self.show_policy

    def test_equality(self, artist_skeleton_source):
        a = ArtistSkeletonBlockData(source=artist_skeleton_source, title='A')
        b = ArtistSkeletonBlockData(source=None, title='B')
        c = ArtistSkeletonBlockData(source=artist_skeleton_source, title='A')

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
