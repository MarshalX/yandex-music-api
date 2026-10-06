from typing import Dict, Optional

from yandex_music import AlbumEvent, ArtistEvent, Client, Event, JSONType, Track


class TestEvent:
    id = '9DAmz0UE'
    type = 'tracks'
    type_for_from = 'tracks-by-genre'
    title = 'Нравится электроника? Попробуйте послушать это'
    message: Optional[str] = None
    device: Optional[str] = None
    tracks_count: Optional[int] = None
    genre = 'electronics'

    def test_expected_values(
        self, event: Event, track: Track, artist_event: ArtistEvent, album_event: AlbumEvent
    ) -> None:
        assert event.id == self.id
        assert event.type == self.type
        assert event.type_for_from == self.type_for_from
        assert event.title == self.title
        assert event.tracks == [track]
        assert event.artists == [artist_event]
        assert event.albums == [album_event]
        assert event.message == self.message
        assert event.device == self.device
        assert event.tracks_count == self.tracks_count
        assert event.genre == self.genre

    def test_de_json_none(self, client: Client) -> None:
        assert Event.de_json({}, client) is None

    def test_de_list_none(self, client: Client) -> None:
        assert Event.de_list([], client) == []

    def test_de_json_required(self, client: Client) -> None:
        json_dict: Dict[str, JSONType] = {'id': self.id, 'type': self.type}
        event = Event.de_json(json_dict, client)
        assert event is not None

        assert event.id == self.id
        assert event.type == self.type

    def test_de_json_all(
        self, client: Client, track: Track, artist_event: ArtistEvent, album_event: AlbumEvent
    ) -> None:
        json_dict: Dict[str, JSONType] = {
            'id': self.id,
            'type': self.type,
            'type_for_from': self.type_for_from,
            'title': self.title,
            'tracks': [track.to_dict()],
            'artists': [artist_event.to_dict()],
            'albums': [album_event.to_dict()],
            'message': self.message,
            'device': self.device,
            'tracks_count': self.tracks_count,
            'genre': self.genre,
        }
        event = Event.de_json(json_dict, client)
        assert event is not None

        assert event.id == self.id
        assert event.type == self.type
        assert event.type_for_from == self.type_for_from
        assert event.title == self.title
        assert event.tracks == [track]
        assert event.artists == [artist_event]
        assert event.albums == [album_event]
        assert event.message == self.message
        assert event.device == self.device
        assert event.tracks_count == self.tracks_count
        assert event.genre == self.genre

    def test_equality(self) -> None:
        a = Event(self.id, self.type)
        b = Event(self.id, '')
        c = Event(self.id, self.type, self.type_for_from)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
