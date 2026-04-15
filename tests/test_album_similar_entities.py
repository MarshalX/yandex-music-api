from yandex_music import AlbumSimilarEntities


class TestAlbumSimilarEntities:
    def test_expected_value(self, album_similar_entities, similar_entity_item):
        assert album_similar_entities.items == [similar_entity_item]

    def test_de_json_none(self, client):
        assert AlbumSimilarEntities.de_json({}, client) is None

    def test_de_json_all(self, client, similar_entity_item):
        json_dict = {
            'items': [similar_entity_item.to_dict()],
        }
        album_similar_entities = AlbumSimilarEntities.de_json(json_dict, client)

        assert album_similar_entities.items == [similar_entity_item]

    def test_equality(self, similar_entity_item):
        a = AlbumSimilarEntities(items=[similar_entity_item])
        b = AlbumSimilarEntities(items=None)
        c = AlbumSimilarEntities(items=[similar_entity_item])

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
