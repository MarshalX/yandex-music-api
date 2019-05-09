from yandex_music import YandexMusicObject


class InvocationInfo(YandexMusicObject):
    def __init__(self,
                 hostname,
                 req_id,
                 exec_duration_millis,
                 client=None,
                 **kwargs):
        self.hostname = hostname
        self.req_id = req_id
        self.exec_duration_millis = int(exec_duration_millis)

        self.client = client
        self._id_attrs = (self.req_id,)

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(InvocationInfo, cls).de_json(data, client)

        return cls(client=client, **data)
