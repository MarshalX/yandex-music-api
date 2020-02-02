from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client, User, CaseForms


class MadeFor(YandexMusicObject):
    """Класс, представляющий пользователя, для которого был сделан плейлист.

    Attributes:
        user_info (:obj:`yandex_music.User`): Объект класса :class:`yandex_music.User`, представляющий пользователя,
            для которого был сделан плейлист.
        case_forms (:obj:`yandex_music.CaseForms`): Объект класса :class:`yandex_music.CaseForms`, представляющий
            склонение имени пользователя, для которого был сделан плейлист.
        client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

    Args:
        user_info (:obj:`yandex_music.User`): Объект класса :class:`yandex_music.User`, представляющий пользователя,
            для которого был сделан плейлист.
        case_forms (:obj:`yandex_music.CaseForms`): Объект класса :class:`yandex_music.CaseForms`, представляющий
            склонение имени пользователя, для которого был сделан плейлист.
        client (:obj:`yandex_music.Client`, optional): Объект класса :class:`yandex_music.Client`, представляющий клиент
            Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

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
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client`, представляющий клиент
                Yandex Music.

        Returns:
            :obj:`yandex_music.MadeFor`: Объект класса :class:`yandex_music.MadeFor`.
        """
        if not data:
            return None

        data = super(MadeFor, cls).de_json(data, client)
        from yandex_music import User, CaseForms
        data['user_info'] = User.de_json(data.get('user_info'), client)
        data['case_forms'] = CaseForms.de_json(data.get('case_forms'), client)

        return cls(client=client, **data)
