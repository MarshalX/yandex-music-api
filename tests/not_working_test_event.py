import pytest

from yandex_music import Event


@pytest.fixture(scope='class')
def event(tracks, artists, albums):
    return Event(TestEvent.id, TestEvent.type, TestEvent.type_for_from, TestEvent.title, tracks, artists, albums,
                 TestEvent.message, TestEvent.device, TestEvent.tracks_count)


class TestEvent:
    type = None
    type_for_from = None
    title = None
    message = None
    device = None
    tracks_count = None

    def test_expected_values(self, event, id, tracks, artists, albums):
        assert event.id == id
        assert event.type == self.type
        assert event.type_for_from == self.type_for_from
        assert event.title == self.title
        assert event.tracks == tracks
        assert event.artists == artists
        assert event.albums == albums
        assert event.message == self.message
        assert event.device == self.device
        assert event.tracks_count == self.tracks_count

    def test_de_json_required(self, client, id):
        json_dict = {'id': id, 'type': self.type}
        event = Event.de_json(json_dict, client)

        assert event.id == id
        assert event.type == self.type

    def test_de_json_all(self, client, id, tracks, artists, albums):
        json_dict = {'id': id, 'type': self.type, 'type_for_from': self.type_for_from, 'title': self.title,
                     'tracks': tracks, 'artists': artists, 'albums': albums, 'message': self.message,
                     'device': self.device, 'tracks_count': self.tracks_count}
        event = Event.de_json(json_dict, client)

        assert event.id == id
        assert event.type == self.type
        assert event.type_for_from == self.type_for_from
        assert event.title == self.title
        assert event.tracks == tracks
        assert event.artists == artists
        assert event.albums == albums
        assert event.message == self.message
        assert event.device == self.device
        assert event.tracks_count == self.tracks_count

    def test_equality(self):
        pass
