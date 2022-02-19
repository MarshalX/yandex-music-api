from typing import TYPE_CHECKING, Optional, List

from yandex_music import YandexMusicObject
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client, PlaylistId


@model
class TagResult(YandexMusicObject):
    """Класс, представляющий тег и его плейлисты.

    Attributes:
        tag (:obj:`yandex_music.Tag`): Тег.
        ids (:obj:`list` из :obj:`yandex_music.PlaylistId`): Уникальные идентификаторы плейлистов тега.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    tag: str
    ids: List['PlaylistId']
    client: Optional['Client'] = None

    def __post_init__(self):
        self._id_attrs = (self.tag, self.ids)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['TagResult']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.TagResult`: Тег и его плейлисты.
        """
        if not data:
            return None

        data = super(TagResult, cls).de_json(data, client)
        from yandex_music import Tag, PlaylistId

        data['tag'] = Tag.de_json(data.get('tag'), client)
        data['ids'] = PlaylistId.de_list(data.get('ids'), client)

        return cls(client=client, **data)

    # TODO (MarshalX) add fetch_playlists shortcut?
