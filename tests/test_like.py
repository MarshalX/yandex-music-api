from typing import Dict, Optional, Tuple

import pytest

from yandex_music import Album, Artist, Client, JSONType, Like, Playlist, YandexMusicModel


def make_like(
    type_: str,
    id_: Optional[int],
    timestamp: Optional[str],
    result: YandexMusicModel,
    short_description: Optional[str] = None,
    description: Optional[str] = None,
    is_premiere: Optional[bool] = None,
    is_banner: Optional[bool] = None,
) -> Like:
    return Like(
        type_,
        id_,
        timestamp,
        album=result if isinstance(result, Album) else None,
        artist=result if isinstance(result, Artist) else None,
        playlist=result if isinstance(result, Playlist) else None,
        short_description=short_description,
        description=description,
        is_premiere=is_premiere,
        is_banner=is_banner,
    )


@pytest.fixture(scope='class', params=[2, 3, 4])
def like_with_param(
    request: pytest.FixtureRequest, results: Dict[int, YandexMusicModel], types: Dict[int, str]
) -> Tuple[Like, int]:
    return (
        make_like(
            types[request.param],
            TestLike.id,
            TestLike.timestamp,
            results[request.param],
            short_description=TestLike.short_description,
            description=TestLike.description,
            is_premiere=TestLike.is_premiere,
            is_banner=TestLike.is_banner,
        ),
        request.param,
    )


class TestLike:
    id = 5246018
    timestamp = '2019-09-03T19:59:56+00:00'
    short_description = 'Учим английский нескучно'
    description = (
        'Английский по песням – это аудио- и видеоподкаст радио Unistar о том, как учить английский язык '
        'по песням – хитам 90-х и 2000-х, которые звучат на Unistar. Никакого занудства, грамматических '
        'правил и зубрежки. Только нескучный английский! Вы узнаете, о чем поют в любимых песнях, и как '
        'это может помочь вам в общении во время путешествий.'
    )
    is_premiere = False
    is_banner = True

    def test_expected_values(
        self, results: Dict[int, YandexMusicModel], types: Dict[int, str], like_with_param: Tuple[Like, int]
    ) -> None:
        like, param = like_with_param

        assert like.type == types[param]
        assert like.id == self.id
        assert like.timestamp == self.timestamp
        assert like.short_description == self.short_description
        assert like.description == self.description
        assert like.is_premiere == self.is_premiere
        assert like.is_banner == self.is_banner
        assert getattr(like, like.type) == results[param]

    def test_de_json_none(self, client: Client) -> None:
        assert Like.de_json({}, client) is None

    def test_de_list_none(self, client: Client) -> None:
        assert Like.de_list([], client) == []

    @pytest.mark.parametrize('param', [2, 3, 4])
    def test_de_json_all(
        self, results: Dict[int, YandexMusicModel], types: Dict[int, str], client: Client, param: int
    ) -> None:
        result, type_ = results[param], types[param]

        json_dict: Dict[str, JSONType] = {
            'timestamp': self.timestamp,
            'id': self.id,
            type_: result.to_dict(),
            'short_description': self.short_description,
            'description': self.description,
            'is_premiere': self.is_premiere,
            'is_banner': self.is_banner,
        }
        like = Like.de_json(json_dict, client, type_)
        assert like is not None

        assert like.type == type_
        assert like.id == self.id
        assert like.timestamp == self.timestamp
        assert like.short_description == self.short_description
        assert like.description == self.description
        assert like.is_premiere == self.is_premiere
        assert like.is_banner == self.is_banner
        assert getattr(like, type_) == result

    @pytest.mark.parametrize('param', [2, 3, 4])
    def test_equality(self, results: Dict[int, YandexMusicModel], types: Dict[int, str], param: int) -> None:
        result, type_ = results[param], types[param]

        a = make_like(type_, self.id, self.timestamp, result)
        b = make_like(type_, 0, self.timestamp, result)
        c = make_like(type_, self.id, '', result)
        d = make_like(type_, self.id, self.timestamp, result)

        assert a != b != c
        assert hash(a) != hash(b) != hash(c)
        assert a is not b is not c

        assert a == d
