from yandex_music import InvocationInfo


class TestInvocationInfo:
    hostname = None
    req_id = None
    exec_duration_millis = None

    def test_expected_values(self, invocation_info):
        assert invocation_info.hostname == self.hostname
        assert invocation_info.req_id == self.req_id
        assert invocation_info.exec_duration_millis == self.exec_duration_millis

    def test_de_json_required(self, client):
        json_dict = {'hostname': self.hostname, 'req_id': self.req_id}
        invocation_info = InvocationInfo.de_json(json_dict, client)

        assert invocation_info.hostname == self.hostname
        assert invocation_info.req_id == self.req_id

    def test_de_json_all(self, client):
        json_dict = {'hostname': self.hostname, 'req_id': self.req_id,
                     'exec_duration_millis': self.exec_duration_millis}
        invocation_info = InvocationInfo.de_json(json_dict, client)

        assert invocation_info.hostname == self.hostname
        assert invocation_info.req_id == self.req_id
        assert invocation_info.exec_duration_millis == self.exec_duration_millis

    def test_equality(self):
        pass
