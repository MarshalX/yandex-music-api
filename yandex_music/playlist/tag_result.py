from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType, PlaylistId


@model
class TagResult(YandexMusicModel):
    """Класс, представляющий тег и его плейлисты.

    Attributes:
        tag (:obj:`yandex_music.Tag`): Тег.
        ids (:obj:`list` из :obj:`yandex_music.PlaylistId`): Уникальные идентификаторы плейлистов тега.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    tag: str
    ids: List['PlaylistId']
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.tag, self.ids)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['TagResult']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.TagResult`: Тег и его плейлисты.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)
        from yandex_music import PlaylistId, Tag

        cls_data['tag'] = Tag.de_json(data.get('tag'), client)
        cls_data['ids'] = PlaylistId.de_list(data.get('ids'), client)

        return cls(client=client, **cls_data)  # type: ignore

    # TODO (MarshalX) add fetch_playlists shortcut?
    #  https://github.com/MarshalX/yandex-music-api/issues/551
