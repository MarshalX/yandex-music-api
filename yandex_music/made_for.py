from yandex_music import YandexMusicObject


class MadeFor(YandexMusicObject):
    def __init__(self,
                 user_info,
                 case_forms,
                 client=None,
                 **kwargs):
        self.user_info = user_info
        self.case_forms = case_forms

        self.client = client

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(MadeFor, cls).de_json(data, client)
        from yandex_music import User, CaseForms
        data['user_info'] = User.de_json(data.get('user_info'), client)
        data['case_forms'] = CaseForms.de_json(data.get('case_forms'), client)

        return cls(client=client, **data)
