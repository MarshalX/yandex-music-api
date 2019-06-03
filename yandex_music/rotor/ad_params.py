from yandex_music import YandexMusicObject


class AdParams(YandexMusicObject):
    def __init__(self,
                 partner_id,
                 category_id,
                 page_ref,
                 target_ref,
                 other_params,
                 ad_volume,
                 genre_id=None,
                 genre_name=None,
                 client=None,
                 **kwargs):
        self.partner_id = partner_id
        self.category_id = category_id
        self.page_ref = page_ref
        self.target_ref = target_ref
        self.other_params = other_params
        self.ad_volume = ad_volume

        self.genre_id = genre_id
        self.genre_name = genre_name

        self.client = client

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(AdParams, cls).de_json(data, client)

        return cls(client=client, **data)
