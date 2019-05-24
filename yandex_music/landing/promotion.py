from yandex_music import YandexMusicObject


class Promotion(YandexMusicObject):
    def __init__(self,
                 promo_id,
                 title,
                 subtitle,
                 heading,
                 url,
                 url_scheme,
                 text_color,
                 gradient,
                 image,
                 client=None,
                 **kwargs):
        self.promo_id = promo_id
        self.title = title
        self.subtitle = subtitle
        self.heading = heading
        self.url = url
        self.url_scheme = url_scheme
        self.text_color = text_color
        self.gradient = gradient
        self.image = image

        self.client = client

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(Promotion, cls).de_json(data, client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data, client):
        if not data:
            return []

        promotions = list()
        for promotion in data:
            promotions.append(cls.de_json(promotion, client))

        return promotions
