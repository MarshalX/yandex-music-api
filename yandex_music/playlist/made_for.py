from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from yandex_music import Client, User, CaseForms

from yandex_music import YandexMusicObject


class MadeFor(YandexMusicObject):
    def __init__(self,
                 user_info: Optional['User'],
                 case_forms: Optional['CaseForms'],
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        self.user_info = user_info
        self.case_forms = case_forms

        self.client = client
        self._id_attrs = (self.user_info, self.case_forms)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['MadeFor']:
        if not data:
            return None

        data = super(MadeFor, cls).de_json(data, client)
        from yandex_music import User, CaseForms
        data['user_info'] = User.de_json(data.get('user_info'), client)
        data['case_forms'] = CaseForms.de_json(data.get('case_forms'), client)

        return cls(client=client, **data)
