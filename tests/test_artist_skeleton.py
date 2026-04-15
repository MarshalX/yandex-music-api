from yandex_music import ArtistSkeleton


class TestArtistSkeleton:
    id = 'web-artist-default'
    title = 'Артист'

    def test_expected_value(self, artist_skeleton, artist_skeleton_block):
        assert artist_skeleton.id == self.id
        assert artist_skeleton.title == self.title
        assert artist_skeleton.blocks == [artist_skeleton_block]

    def test_de_json_none(self, client):
        assert ArtistSkeleton.de_json({}, client) is None

    def test_de_json_all(self, client, artist_skeleton_block):
        json_dict = {
            'id': self.id,
            'title': self.title,
            'blocks': [artist_skeleton_block.to_dict()],
        }
        obj = ArtistSkeleton.de_json(json_dict, client)

        assert obj.id == self.id
        assert obj.title == self.title

    def test_equality(self):
        a = ArtistSkeleton(id='a', title='A')
        b = ArtistSkeleton(id='b', title='B')
        c = ArtistSkeleton(id='a', title='A')

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
