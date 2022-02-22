import pytest

from yandex_music import Like


@pytest.fixture(scope='class', params=[2, 3, 4])
def like_with_param(request, results, types):
    return (
        Like(
            types[request.param],
            TestLike.id,
            TestLike.timestamp,
            short_description=TestLike.short_description,
            description=TestLike.description,
            is_premiere=TestLike.is_premiere,
            is_banner=TestLike.is_banner,
            **{types[request.param]: results[request.param]},
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

    def test_expected_values(self, results, types, like_with_param):
        like, param = like_with_param

        assert like.type == types[param]
        assert like.id == self.id
        assert like.timestamp == self.timestamp
        assert like.short_description == self.short_description
        assert like.description == self.description
        assert like.is_premiere == self.is_premiere
        assert like.is_banner == self.is_banner
        assert getattr(like, like.type) == results[param]

    def test_de_json_none(self, client):
        assert Like.de_json({}, client) is None

    def test_de_list_none(self, client):
        assert Like.de_list({}, client) == []

    @pytest.mark.parametrize('param', [2, 3, 4])
    def test_de_json_all(self, results, types, client, param):
        result, type_ = results[param], types[param]

        json_dict = {
            'timestamp': self.timestamp,
            'id': self.id,
            type_: result.to_dict(),
            'short_description': self.short_description,
            'description': self.description,
            'is_premiere': self.is_premiere,
            'is_banner': self.is_banner,
        }
        like = Like.de_json(json_dict, client, type_)

        assert like.type == type_
        assert like.id == self.id
        assert like.timestamp == self.timestamp
        assert like.short_description == self.short_description
        assert like.description == self.description
        assert like.is_premiere == self.is_premiere
        assert like.is_banner == self.is_banner
        assert getattr(like, type_) == result

    @pytest.mark.parametrize('param', [2, 3, 4])
    def test_equality(self, results, types, param):
        result, type_ = results[param], types[param]

        a = Like(type_, self.id, self.timestamp, **{type_: result})
        b = Like(type_, '', self.timestamp, **{type_: result})
        c = Like(type_, self.id, '', **{type_: result})
        d = Like(type_, self.id, self.timestamp, **{type_: result})

        assert a != b != c
        assert hash(a) != hash(b) != hash(c)
        assert a is not b is not c

        assert a == d
