from typing import Dict

from yandex_music import Client, JSONType, SkeletonBlockData, SkeletonSource, SkeletonViewAllAction


class TestSkeletonBlockData:
    selected_tab_index = 0
    title = 'Популярные треки'
    show_policy = 'SHOW_AND_LOAD'

    def test_expected_value(
        self,
        skeleton_block_data: SkeletonBlockData,
        skeleton_source: SkeletonSource,
        skeleton_view_all_action: SkeletonViewAllAction,
    ) -> None:
        assert skeleton_block_data.source == skeleton_source
        assert skeleton_block_data.title == self.title
        assert skeleton_block_data.show_policy == self.show_policy
        assert skeleton_block_data.view_all_action == skeleton_view_all_action

    def test_de_json_none(self, client: Client) -> None:
        assert SkeletonBlockData.de_json({}, client) is None

    def test_de_json_all(
        self, client: Client, skeleton_source: SkeletonSource, skeleton_view_all_action: SkeletonViewAllAction
    ) -> None:
        json_dict: Dict[str, JSONType] = {
            'source': skeleton_source.to_dict(),
            'title': self.title,
            'showPolicy': self.show_policy,
            'viewAllAction': skeleton_view_all_action.to_dict(),
        }
        obj = SkeletonBlockData.de_json(json_dict, client)
        assert obj is not None

        assert obj.source == skeleton_source
        assert obj.title == self.title
        assert obj.show_policy == self.show_policy

    def test_equality(self, skeleton_source: SkeletonSource) -> None:
        a = SkeletonBlockData(source=skeleton_source, title='A')
        b = SkeletonBlockData(source=None, title='B')
        c = SkeletonBlockData(source=skeleton_source, title='A')

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
