from datetime import datetime

from yandex_music import YandexMusicObject, PassportPhone


class Account(YandexMusicObject):
    def __init__(self,
                 now,
                 uid,
                 login,
                 region,
                 full_name,
                 second_name,
                 first_name,
                 display_name,
                 birthday,
                 service_available,
                 hosted_user,
                 passport_phones,
                 registered_at,
                 has_info_for_app_metrica=False,
                 client=None,
                 **kwargs):
        self.now = datetime.fromisoformat(now)
        self.uid = uid
        self.login = login
        self.region = region
        self.full_name = full_name
        self.second_name = second_name
        self.first_name = first_name
        self.display_name = display_name
        self.birthday = datetime.fromisoformat(birthday)
        self.service_available = bool(service_available)
        self.hosted_user = bool(hosted_user)
        self.passport_phones = passport_phones
        self.registered_at = datetime.fromisoformat(registered_at)
        self.has_info_for_app_metrica = bool(has_info_for_app_metrica)

        self.client = client
        self._id_attrs = (self.uid,)

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None

        data = super(Account, cls).de_json(data, client)
        data['passport_phones'] = PassportPhone.de_list(data.get('passport_phones'), client)

        return cls(client=client, **data)
