from yandex_music import YandexMusicObject


class CaptchaResponse(YandexMusicObject):
    def __init__(self,
                 x_captcha_url,
                 x_captcha_key,
                 error_description,
                 error,
                 client=None,
                 **kwargs):
        self.x_captcha_url = x_captcha_url
        self.x_captcha_key = x_captcha_key
        self.error_description = error_description
        self.error = error

        self.client = client

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(CaptchaResponse, cls).de_json(data, client)

        return cls(client=client, **data)
