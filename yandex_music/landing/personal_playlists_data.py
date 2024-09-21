from typing import TYPE_CHECKING, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType


@model
class PersonalPlaylistsData(YandexMusicModel):
    """Класс, представляющий дополнительную информацию о персональном плейлисте.

    Attributes:
        is_wizard_passed (:obj:`bool`): TODO.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    is_wizard_passed: bool
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.is_wizard_passed,)
