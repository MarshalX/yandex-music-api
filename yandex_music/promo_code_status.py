from yandex_music import YandexMusicObject


class PromoCodeStatus(YandexMusicObject):
    def __init__(self,
                 status,
                 status_desc,
                 account_status,
                 client=None,
                 **kwargs):
        self.status = status
        self.status_desc = status_desc
        self.account_status = account_status

        self.client = client

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(PromoCodeStatus, cls).de_json(data, client)
        from yandex_music import Status
        data['account_status'] = Status.de_json(data.get('account_status'), client)

        return cls(client=client, **data)
