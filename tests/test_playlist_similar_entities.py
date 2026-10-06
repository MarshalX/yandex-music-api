from typing import Dict

from yandex_music import Client, JSONType, PlaylistSimilarEntities, SimilarEntityItem


class TestPlaylistSimilarEntities:
    def test_expected_value(
        self, playlist_similar_entities: PlaylistSimilarEntities, similar_entity_item: SimilarEntityItem
    ) -> None:
        assert playlist_similar_entities.items == [similar_entity_item]

    def test_de_json_none(self, client: Client) -> None:
        assert PlaylistSimilarEntities.de_json({}, client) is None

    def test_de_json_all(self, client: Client, similar_entity_item: SimilarEntityItem) -> None:
        json_dict: Dict[str, JSONType] = {
            'items': [similar_entity_item.to_dict()],
        }
        playlist_similar_entities = PlaylistSimilarEntities.de_json(json_dict, client)
        assert playlist_similar_entities is not None

        assert playlist_similar_entities.items == [similar_entity_item]

    def test_equality(self, similar_entity_item: SimilarEntityItem) -> None:
        a = PlaylistSimilarEntities(items=[similar_entity_item])
        b = PlaylistSimilarEntities(items=None)
        c = PlaylistSimilarEntities(items=[similar_entity_item])

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
