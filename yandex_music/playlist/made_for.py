from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicObject
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client, User, CaseForms


@model
class MadeFor(YandexMusicObject):
    """Класс, представляющий пользователя, для которого был сделан плейлист.

    Attributes:
        user_info (:obj:`yandex_music.User`): Пользователь, для которого был сделан плейлист.
        case_forms (:obj:`yandex_music.CaseForms`): Склонение имени пользователя, для которого был сделан плейлист.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    user_info: Optional['User']
    case_forms: Optional['CaseForms']
    client: Optional['Client'] = None

    def __post_init__(self):
        self._id_attrs = (self.user_info, self.case_forms)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['MadeFor']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.MadeFor`: Пользователь, для которого был сделан плейлист.
        """
        if not data:
            return None

        data = super(MadeFor, cls).de_json(data, client)
        from yandex_music import User, CaseForms

        data['user_info'] = User.de_json(data.get('user_info'), client)
        data['case_forms'] = CaseForms.de_json(data.get('case_forms'), client)

        return cls(client=client, **data)
