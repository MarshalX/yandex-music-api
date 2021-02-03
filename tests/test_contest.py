from yandex_music import Contest


class TestContest:
    contest_id = 'disco_contest'
    status = 'withdrew-moderator'
    can_edit = True
    sent = '2019-10-22T09:41:54+00:00'
    withdrawn = '2019-10-23T07:02:03+00:00'

    def test_expected_values(self, contest):
        assert contest.contest_id == self.contest_id
        assert contest.status == self.status
        assert contest.can_edit == self.can_edit
        assert contest.sent == self.sent
        assert contest.withdrawn == self.withdrawn

    def test_de_json_none(self, client):
        assert Contest.de_json({}, client) is None

    def test_de_json_required(self, client):
        json_dict = {'contest_id': self.contest_id, 'status': self.status, 'can_edit': self.can_edit}
        contest = Contest.de_json(json_dict, client)

        assert contest.contest_id == self.contest_id
        assert contest.status == self.status
        assert contest.can_edit == self.can_edit

    def test_de_json_all(self, client):
        json_dict = {
            'contest_id': self.contest_id,
            'status': self.status,
            'can_edit': self.can_edit,
            'sent': self.sent,
            'withdrawn': self.withdrawn,
        }
        contest = Contest.de_json(json_dict, client)

        assert contest.contest_id == self.contest_id
        assert contest.status == self.status
        assert contest.can_edit == self.can_edit
        assert contest.sent == self.sent
        assert contest.withdrawn == self.withdrawn

    def test_equality(self):
        a = Contest(self.contest_id, self.status, self.can_edit)
        b = Contest('', self.status, self.can_edit)
        c = Contest(self.contest_id, self.status, self.can_edit)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
