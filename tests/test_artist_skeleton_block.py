from yandex_music import ArtistSkeletonBlock


class TestArtistSkeletonBlock:
    id = 'artist_popular_tracks'
    type = 'ARTIST_POPULAR_TRACKS'

    def test_expected_value(self, artist_skeleton_block, artist_skeleton_block_data):
        assert artist_skeleton_block.id == self.id
        assert artist_skeleton_block.type == self.type
        assert artist_skeleton_block.data == artist_skeleton_block_data

    def test_de_json_none(self, client):
        assert ArtistSkeletonBlock.de_json({}, client) is None

    def test_de_json_all(self, client, artist_skeleton_block_data):
        json_dict = {
            'id': self.id,
            'type': self.type,
            'data': artist_skeleton_block_data.to_dict(),
        }
        obj = ArtistSkeletonBlock.de_json(json_dict, client)

        assert obj.id == self.id
        assert obj.type == self.type
        assert obj.data.source == artist_skeleton_block_data.source
        assert obj.data.title == artist_skeleton_block_data.title

    def test_equality(self):
        a = ArtistSkeletonBlock(id='a', type='A')
        b = ArtistSkeletonBlock(id='b', type='B')
        c = ArtistSkeletonBlock(id='a', type='A')

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
