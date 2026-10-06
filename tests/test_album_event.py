from typing import Dict

from yandex_music import Album, AlbumEvent, ArtistEvent, Client, JSONType, Track


class TestAlbumEvent:
    def test_expected_values(self, album_event: AlbumEvent, album: Album, track: Track) -> None:
        assert album_event.album == album
        assert album_event.tracks == [track]

    def test_de_json_none(self, client: Client) -> None:
        assert AlbumEvent.de_json({}, client) is None

    def test_de_list_none(self, client: Client) -> None:
        assert AlbumEvent.de_list([], client) == []

    def test_de_json_required(self, client: Client, album: Album, track: Track) -> None:
        json_dict: Dict[str, JSONType] = {'album': album.to_dict(), 'tracks': [track.to_dict()]}
        album_event = AlbumEvent.de_json(json_dict, client)
        assert album_event is not None

        assert album_event.album == album
        assert album_event.tracks == [track]

    def test_de_json_all(self, client: Client, album: Album, track: Track) -> None:
        json_dict: Dict[str, JSONType] = {'album': album.to_dict(), 'tracks': [track.to_dict()]}
        album_event = AlbumEvent.de_json(json_dict, client)
        assert album_event is not None

        assert album_event.album == album
        assert album_event.tracks == [track]

    def test_equality(self, album: Album, track: Track, artist_event: ArtistEvent) -> None:
        a = AlbumEvent(album, [track])
        b = AlbumEvent(None, [track])
        c = AlbumEvent(album, [track])

        assert a != b != artist_event
        assert hash(a) != hash(b) != hash(artist_event)
        assert a is not b is not artist_event

        assert a == c
