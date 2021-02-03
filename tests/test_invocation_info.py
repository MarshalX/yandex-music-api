from yandex_music import InvocationInfo


class TestInvocationInfo:
    hostname = 'myt1-0261-c2e-msk-myt-music-st-e72-18274.gencfg-c.yandex.net'
    req_id = '1573172241066040-16981638052883278246'
    exec_duration_millis = 0

    def test_expected_values(self, invocation_info):
        assert invocation_info.hostname == self.hostname
        assert invocation_info.req_id == self.req_id
        assert invocation_info.exec_duration_millis == self.exec_duration_millis

    def test_de_json_none(self, client):
        assert InvocationInfo.de_json({}, client) is None

    def test_de_json_required(self, client):
        json_dict = {'hostname': self.hostname, 'req_id': self.req_id}
        invocation_info = InvocationInfo.de_json(json_dict, client)

        assert invocation_info.hostname == self.hostname
        assert invocation_info.req_id == self.req_id

    def test_de_json_all(self, client):
        json_dict = {
            'hostname': self.hostname,
            'req_id': self.req_id,
            'exec_duration_millis': self.exec_duration_millis,
        }
        invocation_info = InvocationInfo.de_json(json_dict, client)

        assert invocation_info.hostname == self.hostname
        assert invocation_info.req_id == self.req_id
        assert invocation_info.exec_duration_millis == self.exec_duration_millis

    def test_equality(self):
        a = InvocationInfo(self.hostname, self.req_id)
        b = InvocationInfo('', self.req_id, 0)
        c = InvocationInfo(self.hostname, self.req_id, 20)

        assert a != b
        assert hash(a) != hash(b)
        assert a is not b

        assert a == c
