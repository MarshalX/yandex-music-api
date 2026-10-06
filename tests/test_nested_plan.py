from typing import Dict, List, Optional, Set

import pytest

from yandex_music import Album, Client, Genre, JSONType, Track, YandexMusicModel
from yandex_music.utils import model


def _all_models() -> List[type]:
    models: Set[type] = set()
    stack: List[type] = [YandexMusicModel]
    while len(stack) > 0:
        klass = stack.pop()
        for subclass in klass.__subclasses__():
            if subclass not in models:
                models.add(subclass)
                stack.append(subclass)
    return sorted(models, key=lambda klass: f'{klass.__module__}.{klass.__qualname__}')


@pytest.mark.parametrize('klass', _all_models(), ids=lambda klass: klass.__qualname__)
def test_nested_plan_resolves(klass: type) -> None:
    assert issubclass(klass, YandexMusicModel)
    _ = klass.nested_plan()


@model
class _Leaf(YandexMusicModel):
    value: Optional[int] = None
    client: Optional['Client'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.value,)


@model
class _Node(YandexMusicModel):
    leaf: Optional[_Leaf] = None
    leaves: Optional[List[_Leaf]] = None
    matrix: Optional[List[List[_Leaf]]] = None
    mapping: Optional[Dict[str, _Leaf]] = None
    raw: Optional[Dict[str, JSONType]] = None
    title: Optional[str] = None
    client: Optional['Client'] = None


class TestNestedPlan:
    def test_plan_fields(self) -> None:
        assert [name for name, _ in _Node.nested_plan()] == ['leaf', 'leaves', 'matrix', 'mapping']

    def test_plan_cached(self) -> None:
        assert _Node.nested_plan() is _Node.nested_plan()

    def test_de_json_nested(self, client: Client) -> None:
        node = _Node.de_json(
            {
                'leaf': {'value': 1},
                'leaves': [{'value': 2}],
                'matrix': [[{'value': 3}], [{'value': 4}]],
                'mapping': {'a': {'value': 5}},
                'raw': {'value': 6},
                'title': 'title',
            },
            client,
        )
        assert node is not None

        assert node.leaf == _Leaf(value=1)
        assert node.leaves == [_Leaf(value=2)]
        assert node.matrix == [[_Leaf(value=3)], [_Leaf(value=4)]]
        assert node.mapping == {'a': _Leaf(value=5)}
        assert node.raw == {'value': 6}
        assert node.title == 'title'
        assert node.leaf is not None
        assert node.leaf.client is client

    def test_de_json_missing_nested(self, client: Client) -> None:
        node = _Node.de_json({'title': 'title'}, client)
        assert node is not None

        assert node.leaf is None
        assert node.leaves == []
        assert node.matrix == []
        assert node.mapping == {}
        assert node.raw is None

    def test_de_nested_exclude(self, client: Client) -> None:
        cls_data = _Node.de_nested({'leaf': {'value': 1}, 'leaves': [{'value': 2}]}, client, exclude=('leaf',))

        assert cls_data['leaf'] == {'value': 1}
        assert cls_data['leaves'] == [_Leaf(value=2)]

    def test_real_models(self) -> None:
        assert 'volumes' in dict(Album.nested_plan())
        assert 'labels' not in dict(Album.nested_plan())
        assert 'albums' in dict(Track.nested_plan())
        assert 'titles' in dict(Genre.nested_plan())
