from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import CaseForms, ClientType


@model
class MadeForUser(YandexMusicModel):
    """Класс, представляющий признак персонального плейлиста.

    Attributes:
        is_made_for_user (:obj:`bool`, optional): Сделан ли плейлист для текущего пользователя.
        case_forms (:obj:`yandex_music.CaseForms`, optional): Склонение имени пользователя.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    is_made_for_user: Optional[bool] = None
    case_forms: Optional['CaseForms'] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.is_made_for_user, self.case_forms)
