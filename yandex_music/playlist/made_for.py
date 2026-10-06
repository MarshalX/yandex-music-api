from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import CaseForms, ClientType, User


@model
class MadeFor(YandexMusicModel):
    """Класс, представляющий пользователя, для которого был сделан плейлист.

    Attributes:
        user_info (:obj:`yandex_music.User`): Пользователь, для которого был сделан плейлист.
        case_forms (:obj:`yandex_music.CaseForms`): Склонение имени пользователя, для которого был сделан плейлист.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    user_info: Optional['User']
    case_forms: Optional['CaseForms']
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.user_info, self.case_forms)
