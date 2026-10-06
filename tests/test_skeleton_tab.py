from typing import Dict

from yandex_music import Client, JSONType, SkeletonBlock, SkeletonTab


class TestSkeletonTab:
    id = 'web-artist-default'
    title = 'Артист'

    def test_expected_value(self, skeleton_tab: SkeletonTab, skeleton_block: SkeletonBlock) -> None:
        assert skeleton_tab.id == self.id
        assert skeleton_tab.title == self.title
        assert skeleton_tab.blocks == [skeleton_block]

    def test_de_json_none(self, client: Client) -> None:
        assert SkeletonTab.de_json({}, client) is None

    def test_de_json_all(self, client: Client, skeleton_block: SkeletonBlock) -> None:
        json_dict: Dict[str, JSONType] = {
            'id': self.id,
            'title': self.title,
            'blocks': [skeleton_block.to_dict()],
        }
        obj = SkeletonTab.de_json(json_dict, client)
        assert obj is not None

        assert obj.id == self.id
        assert obj.title == self.title
        assert obj.blocks == [skeleton_block]

    def test_equality(self) -> None:
        a = SkeletonTab(id='a', title='A')
        b = SkeletonTab(id='b', title='B')
        c = SkeletonTab(id='a', title='A')

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
