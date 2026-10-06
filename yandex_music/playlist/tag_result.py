from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, PlaylistId, Tag


@model
class TagResult(YandexMusicModel):
    """Класс, представляющий тег и его плейлисты.

    Attributes:
        tag (:obj:`yandex_music.Tag`): Тег.
        ids (:obj:`list` из :obj:`yandex_music.PlaylistId`): Уникальные идентификаторы плейлистов тега.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    tag: Optional['Tag']
    ids: List['PlaylistId']
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.tag, self.ids)

    # TODO(MarshalX): add fetch_playlists shortcut?
    #  https://github.com/MarshalX/yandex-music-api/issues/551
