from yandex_music import PlaylistAbsence


class TestPlaylistAbsence:
    kind = 1003
    reason = 'playlist-is-deleted'

    def test_expected_values(self, playlist_absence):
        assert playlist_absence.kind == self.kind
        assert playlist_absence.reason == self.reason

    def test_de_json_none(self, client):
        assert PlaylistAbsence.de_json({}, client) is None

    def test_de_json_required(self, client):
        json_dict = {'kind': self.kind, 'reason': self.reason}
        playlist_absence = PlaylistAbsence.de_json(json_dict, client)

        assert playlist_absence.kind == self.kind
        assert playlist_absence.reason == self.reason

    def test_de_json_all(self, client):
        json_dict = {'kind': self.kind, 'reason': self.reason}
        playlist_absence = PlaylistAbsence.de_json(json_dict, client)

        assert playlist_absence.kind == self.kind
        assert playlist_absence.reason == self.reason

    def test_equality(self):
        a = PlaylistAbsence(self.kind, self.reason)
        b = PlaylistAbsence(10, self.reason)
        c = PlaylistAbsence(self.kind, self.reason)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
