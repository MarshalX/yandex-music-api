from typing import Dict

from yandex_music import Artist, Client, ContentRestrictions, JSONType, UpcomingAlbum


class TestUpcomingAlbum:
    id = 100500
    title = 'Предстоящий альбом'
    type = 'single'
    release_date = '2026-12-01T00:00:00+03:00'
    milliseconds_until_release = 864000000
    cover_uri = 'avatars.yandex.net/get-music-content/12345/upcoming/%%'
    presaved = False

    def test_expected_values(
        self, upcoming_album: UpcomingAlbum, artist_without_tracks: Artist, content_restrictions: ContentRestrictions
    ) -> None:
        assert upcoming_album.id == self.id
        assert upcoming_album.title == self.title
        assert upcoming_album.type == self.type
        assert upcoming_album.release_date == self.release_date
        assert upcoming_album.milliseconds_until_release == self.milliseconds_until_release
        assert upcoming_album.cover_uri == self.cover_uri
        assert upcoming_album.presaved == self.presaved
        assert upcoming_album.artists == [artist_without_tracks]
        assert upcoming_album.content_restrictions == content_restrictions

    def test_de_json_none(self, client: Client) -> None:
        assert UpcomingAlbum.de_json({}, client) is None

    def test_de_json_all(self, client: Client, artist: Artist, content_restrictions: ContentRestrictions) -> None:
        json_dict: Dict[str, JSONType] = {
            'id': self.id,
            'title': self.title,
            'type': self.type,
            'releaseDate': self.release_date,
            'millisecondsUntilRelease': self.milliseconds_until_release,
            'coverUri': self.cover_uri,
            'presaved': self.presaved,
            'artists': [artist.to_dict()],
            'contentRestrictions': content_restrictions.to_dict(),
        }
        obj = UpcomingAlbum.de_json(json_dict, client)
        assert obj is not None

        assert obj.id == self.id
        assert obj.title == self.title
        assert obj.type == self.type
        assert obj.release_date == self.release_date
        assert obj.milliseconds_until_release == self.milliseconds_until_release
        assert obj.cover_uri == self.cover_uri
        assert obj.presaved == self.presaved
        assert obj.artists == [artist]
        assert obj.content_restrictions == content_restrictions

    def test_equality(self) -> None:
        a = UpcomingAlbum(id=self.id, title=self.title)
        b = UpcomingAlbum(id=12345, title=self.title)
        c = UpcomingAlbum(id=self.id, title='')

        assert a != b
        assert hash(a) != hash(b)
        assert a == c
