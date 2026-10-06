from typing import Dict, Tuple, Union

import pytest

from yandex_music import (
    Album,
    BlockEntity,
    ChartItem,
    Client,
    GeneratedPlaylist,
    JSONType,
    MixLink,
    PlayContext,
    Playlist,
    Promotion,
    YandexMusicModel,
)

BlockEntityData = Union[GeneratedPlaylist, Promotion, Album, Playlist, ChartItem, PlayContext, MixLink]


def as_block_entity_data(item: YandexMusicModel) -> BlockEntityData:
    assert isinstance(item, (GeneratedPlaylist, Promotion, Album, Playlist, ChartItem, PlayContext, MixLink))
    return item


@pytest.fixture(scope='class', params=[3, 4, 6, 7, 8, 9, 10])
def block_entity_data_with_type(
    request: pytest.FixtureRequest, results: Dict[int, YandexMusicModel], types: Dict[int, str]
) -> Tuple[BlockEntityData, str]:
    return as_block_entity_data(results[request.param]), types[request.param]


@pytest.fixture(scope='class', params=[3, 4, 6, 7, 8, 9, 10])
def block_entity_with_data_and_type(
    request: pytest.FixtureRequest, results: Dict[int, YandexMusicModel], types: Dict[int, str]
) -> Tuple[BlockEntity, BlockEntityData, str]:
    data = as_block_entity_data(results[request.param])
    return (
        BlockEntity(TestBlockEntity.id, types[request.param], data),
        data,
        types[request.param],
    )


class TestBlockEntity:
    id = 'lze0IVH4'
    type = 'personal-playlist'

    def test_expected_values(self, block_entity_with_data_and_type: Tuple[BlockEntity, BlockEntityData, str]) -> None:
        block_entity, data, type_ = block_entity_with_data_and_type

        assert block_entity.id == self.id
        assert block_entity.type == type_
        assert block_entity.data == data

    def test_de_list_none(self, client: Client) -> None:
        assert BlockEntity.de_list([], client) == []

    def test_de_json_none(self, client: Client) -> None:
        assert BlockEntity.de_json({}, client) is None

    def test_de_json_required(self, client: Client, block_entity_data_with_type: Tuple[BlockEntityData, str]) -> None:
        data, type_ = block_entity_data_with_type

        json_dict: Dict[str, JSONType] = {'id': self.id, 'type': type_, 'data': data.to_dict()}
        block_entity = BlockEntity.de_json(json_dict, client)
        assert block_entity is not None

        assert block_entity.id == self.id
        assert block_entity.type == type_
        assert block_entity.data == data

    def test_de_json_all(self, client: Client, block_entity_data_with_type: Tuple[BlockEntityData, str]) -> None:
        data, type_ = block_entity_data_with_type

        json_dict: Dict[str, JSONType] = {'id': self.id, 'type': type_, 'data': data.to_dict()}
        block_entity = BlockEntity.de_json(json_dict, client)
        assert block_entity is not None

        assert block_entity.id == self.id
        assert block_entity.type == type_
        assert block_entity.data == data

    def test_equality(self, block_entity_data_with_type: Tuple[BlockEntityData, str]) -> None:
        data, type = block_entity_data_with_type

        a = BlockEntity(self.id, type, data)
        b = BlockEntity(self.id, '', data)
        c = BlockEntity('', type, data)
        d = BlockEntity(self.id, type, data)

        assert a != b != c
        assert hash(a) != hash(b) != hash(c)
        assert a is not b is not c

        assert a == d
