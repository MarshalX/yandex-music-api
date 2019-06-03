from yandex_music import YandexMusicObject


class Dashboard(YandexMusicObject):
    def __init__(self,
                 dashboard_id,
                 stations,
                 pumpkin,
                 client=None,
                 **kwargs):
        self.dashboard_id = dashboard_id
        self.stations = stations
        self.pumpkin = pumpkin

        self.client = client
        self._id_attrs = (self.dashboard_id, )

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(Dashboard, cls).de_json(data, client)
        from yandex_music import StationResult
        data['stations'] = StationResult.de_list(data.get('stations'), client)

        return cls(client=client, **data)
