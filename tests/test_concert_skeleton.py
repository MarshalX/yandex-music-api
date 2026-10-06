from typing import Dict

from yandex_music import Client, ConcertSkeleton, JSONType, SkeletonBlock


class TestConcertSkeleton:
    id = 'concert_page'
    title = 'Страница концерта'

    def test_expected_value(self, concert_skeleton: ConcertSkeleton, skeleton_block: SkeletonBlock) -> None:
        assert concert_skeleton.id == self.id
        assert concert_skeleton.title == self.title
        assert concert_skeleton.blocks == [skeleton_block]

    def test_de_json_none(self, client: Client) -> None:
        assert ConcertSkeleton.de_json({}, client) is None

    def test_de_json_all(self, client: Client, skeleton_block: SkeletonBlock) -> None:
        json_dict: Dict[str, JSONType] = {
            'id': self.id,
            'title': self.title,
            'blocks': [skeleton_block.to_dict()],
        }
        concert_skeleton = ConcertSkeleton.de_json(json_dict, client)
        assert concert_skeleton is not None

        assert concert_skeleton.id == self.id
        assert concert_skeleton.title == self.title
        assert concert_skeleton.blocks == [skeleton_block]

    def test_equality(self, skeleton_block: SkeletonBlock) -> None:
        a = ConcertSkeleton(id=self.id, title=self.title, blocks=[skeleton_block])
        b = ConcertSkeleton(id='other_page', title=self.title, blocks=[skeleton_block])
        c = ConcertSkeleton(id=self.id, title=self.title, blocks=[skeleton_block])

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
