from yandex_music import SkeletonBlock


class TestSkeletonBlock:
    id = 'artist_popular_tracks'
    type = 'ARTIST_POPULAR_TRACKS'

    def test_expected_value(self, skeleton_block, skeleton_block_data):
        assert skeleton_block.id == self.id
        assert skeleton_block.type == self.type
        assert skeleton_block.data == skeleton_block_data

    def test_de_json_none(self, client):
        assert SkeletonBlock.de_json({}, client) is None

    def test_de_json_all(self, client, skeleton_block_data):
        json_dict = {
            'id': self.id,
            'type': self.type,
            'data': skeleton_block_data.to_dict(),
        }
        obj = SkeletonBlock.de_json(json_dict, client)

        assert obj.id == self.id
        assert obj.type == self.type
        assert obj.data.source == skeleton_block_data.source
        assert obj.data.title == skeleton_block_data.title

    def test_equality(self):
        a = SkeletonBlock(id='a', type='A')
        b = SkeletonBlock(id='b', type='B')
        c = SkeletonBlock(id='a', type='A')

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
