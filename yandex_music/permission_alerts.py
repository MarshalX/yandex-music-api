from yandex_music import YandexMusicObject


class PermissionAlerts(YandexMusicObject):
    def __init__(self,
                 alerts,
                 client=None,
                 **kwargs):
        self.alerts = alerts

        self.client = client

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(PermissionAlerts, cls).de_json(data, client)

        return cls(client=client, **data)
