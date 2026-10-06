from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType
    from yandex_music.music_history.music_history_tab import MusicHistoryTab


@model
class MusicHistory(YandexMusicModel):
    """Класс, представляющий историю прослушивания.

    Attributes:
        history_tabs (:obj:`list` из :obj:`yandex_music.MusicHistoryTab`, optional):
            Список вкладок (дней) истории прослушивания.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    history_tabs: Optional[List['MusicHistoryTab']] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.history_tabs,)
