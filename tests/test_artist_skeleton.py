from typing import Dict

from yandex_music import ArtistSkeleton, Client, JSONType, SkeletonBlock


class TestArtistSkeleton:
    id = 'web-artist-default'
    title = 'Артист'

    def test_expected_value(self, artist_skeleton: ArtistSkeleton, skeleton_block: SkeletonBlock) -> None:
        assert artist_skeleton.id == self.id
        assert artist_skeleton.title == self.title
        assert artist_skeleton.blocks == [skeleton_block]

    def test_de_json_none(self, client: Client) -> None:
        assert ArtistSkeleton.de_json({}, client) is None

    def test_de_json_all(self, client: Client, skeleton_block: SkeletonBlock) -> None:
        json_dict: Dict[str, JSONType] = {
            'id': self.id,
            'title': self.title,
            'blocks': [skeleton_block.to_dict()],
        }
        obj = ArtistSkeleton.de_json(json_dict, client)
        assert obj is not None

        assert obj.id == self.id
        assert obj.title == self.title

    def test_equality(self) -> None:
        a = ArtistSkeleton(id='a', title='A')
        b = ArtistSkeleton(id='b', title='B')
        c = ArtistSkeleton(id='a', title='A')

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
