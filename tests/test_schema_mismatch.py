import asyncio
import logging
from dataclasses import field
from typing import Iterator, List, Optional
from unittest.mock import MagicMock
from urllib.parse import parse_qs, urlsplit

import pytest

from yandex_music.base import YandexMusicModel
from yandex_music.exceptions import SchemaMismatchError
from yandex_music.utils import model
from yandex_music.utils.schema_mismatch import (
    SchemaMismatch,
    get_current_endpoint,
    reset_reported,
    sanitize_endpoint,
    set_current_endpoint,
)


@model
class StrictSample(YandexMusicModel):
    id: int
    title: str
    client: Optional[object] = field(default=None, repr=False)
    note: Optional[str] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.id,)


def make_client(strict: bool = False, report_unknown_fields: bool = False) -> MagicMock:
    client = MagicMock()
    client.strict = strict
    client.report_unknown_fields = report_unknown_fields
    client.on_schema_mismatch = None
    return client


@pytest.fixture(autouse=True)
def clean_reported() -> Iterator[None]:
    reset_reported()
    yield
    reset_reported()


class TestLenientConstruct:
    def test_required_fields(self) -> None:
        assert StrictSample.required_fields() == ('id', 'title')

    def test_complete_data(self) -> None:
        obj = StrictSample.de_json({'id': 1, 'title': 'a'}, make_client())
        assert obj is not None
        assert obj.id == 1
        assert obj.title == 'a'

    def test_missing_required_field_does_not_crash(self, caplog: pytest.LogCaptureFixture) -> None:
        with caplog.at_level(logging.WARNING):
            obj = StrictSample.de_json({'id': 1}, make_client())

        assert obj is not None
        assert obj.id == 1
        assert obj.title is None
        assert 'Missing required fields: title' in caplog.text
        assert 'github.com/MarshalX/yandex-music-api/issues/new' in caplog.text

    def test_null_required_field_is_reported(self) -> None:
        reports: List[SchemaMismatch] = []
        client = make_client()
        client.on_schema_mismatch = reports.append

        _ = StrictSample.de_json({'id': 1, 'title': None}, client)

        assert len(reports) == 1
        assert reports[0].missing_fields == {'title'}

    def test_equality_by_id_survives_missing_fields(self) -> None:
        a = StrictSample.de_json({'id': 1}, make_client())
        b = StrictSample.de_json({'id': 1, 'title': 'b'}, make_client())
        assert a == b

    def test_strict_raises(self) -> None:
        with pytest.raises(SchemaMismatchError, match='title'):
            _ = StrictSample.de_json({'id': 1}, make_client(strict=True))

    def test_strict_raises_every_time(self) -> None:
        client = make_client(strict=True)
        for _ in range(2):
            with pytest.raises(SchemaMismatchError):
                _ = StrictSample.de_json({'id': 1}, client)

    def test_no_client(self) -> None:
        obj = StrictSample.construct({'id': 1}, None)
        assert obj.title is None

    def test_list_reports_once(self) -> None:
        reports: List[SchemaMismatch] = []
        client = make_client()
        client.on_schema_mismatch = reports.append

        objs = StrictSample.de_list([{'id': i} for i in range(100)], client)

        assert len(objs) == 100
        assert len(reports) == 1


class TestReporting:
    def test_unknown_fields_go_to_handler(self) -> None:
        reports: List[SchemaMismatch] = []
        client = make_client(report_unknown_fields=True)
        client.on_schema_mismatch = reports.append

        _ = StrictSample.de_json({'id': 1, 'title': 'a', 'newField': 1}, client)

        assert len(reports) == 1
        assert reports[0].unknown_fields == {'new_field'}
        assert reports[0].missing_fields == frozenset()

    def test_unknown_and_missing_in_one_report(self) -> None:
        reports: List[SchemaMismatch] = []
        client = make_client(report_unknown_fields=True)
        client.on_schema_mismatch = reports.append

        _ = StrictSample.de_json({'id': 1, 'newField': 1}, client)

        assert len(reports) == 1
        assert reports[0].missing_fields == {'title'}
        assert reports[0].unknown_fields == {'new_field'}

    def test_unknown_fields_reported_with_custom_de_json(self) -> None:
        from yandex_music import Best

        reports: List[SchemaMismatch] = []
        client = make_client(report_unknown_fields=True)
        client.on_schema_mismatch = reports.append

        _ = Best.de_json({'type': 'track', 'result': None, 'newField': 1}, client)

        assert len(reports) == 1
        assert reports[0].model is Best
        assert reports[0].unknown_fields == {'new_field'}

    def test_report_contains_endpoint(self) -> None:
        reports: List[SchemaMismatch] = []
        client = make_client()
        client.on_schema_mismatch = reports.append

        set_current_endpoint('get', 'https://api.music.yandex.net/users/12345/playlists/3?rich-tracks=true')
        _ = StrictSample.de_json({'id': 1}, client)

        assert reports[0].endpoint == 'GET /users/{id}/playlists/{id}'

    def test_issue_url(self) -> None:
        mismatch = SchemaMismatch(
            model=StrictSample, missing_fields=frozenset({'title'}), endpoint='GET /tracks', version='1.0'
        )
        query = parse_qs(urlsplit(mismatch.issue_url()).query)

        assert query['title'] == ['Отсутствует обязательное поле от API: StrictSample']
        assert query['template'] == ['schema-mismatch.yml']
        assert 'Missing required fields: title' in query['report'][0]
        assert 'GET /tracks' in query['report'][0]


class TestEndpoint:
    @pytest.mark.parametrize(
        ('url', 'expected'),
        [
            ('https://api.music.yandex.net/landing3', 'GET /landing3'),
            ('https://api.music.yandex.net/tracks/123:456/supplement', 'GET /tracks/{id}/supplement'),
            ('https://api.music.yandex.net/users/some.login/likes/tracks', 'GET /users/{id}/likes/tracks'),
            (
                'https://api.music.yandex.net/rotor/station/user:onyourwave/tracks',
                'GET /rotor/station/user:onyourwave/tracks',
            ),
            ('https://api.music.yandex.net/playlist/0f3b2c1a-1111-2222-3333-444455556666', 'GET /playlist/{id}'),
        ],
    )
    def test_sanitize(self, url: str, expected: str) -> None:
        assert sanitize_endpoint('GET', url) == expected

    def test_isolated_between_tasks(self) -> None:
        async def worker(path: str) -> Optional[str]:
            set_current_endpoint('GET', f'https://api.music.yandex.net/{path}')
            await asyncio.sleep(0)
            return get_current_endpoint()

        async def main() -> List[Optional[str]]:
            return list(await asyncio.gather(worker('a'), worker('b')))

        assert asyncio.run(main()) == ['GET /a', 'GET /b']
