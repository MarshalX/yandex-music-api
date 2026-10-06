from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, TrackShortOld


@model
class PlayContext(YandexMusicModel):
    """Класс, представляющий проигрываемый контекст.

    Note:
        Известные значения поля `client_`: `android`.

        Поле `context` хранит в себе место воспроизведения, например, `playlist`.

        Поле `context_item` хранит в себе уникальный идентификатор context'a, т.е. в нашем случае playlist'a.

    Attributes:
        client_ (:obj:`str`): Клиент.
        context (:obj:`str`): Тип контекста.
        context_item (:obj:`str`): Предмет контекста.
        tracks (:obj:`list` из :obj:`yandex_music.TrackShortOld`): Треки.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    client_: str
    context: str
    context_item: str
    tracks: List['TrackShortOld']
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.client_, self.context_item, self.context_item, self.tracks)
