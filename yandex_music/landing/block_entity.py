from typing import TYPE_CHECKING, Optional, Union

from yandex_music import (
    Album,
    ChartItem,
    GeneratedPlaylist,
    MixLink,
    PlayContext,
    Playlist,
    Promotion,
    YandexMusicModel,
)
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import ClientType, JSONType, MapTypeToDeJson

_TYPE_TO_DE_JSON_DEF: 'MapTypeToDeJson' = {
    'personal-playlist': GeneratedPlaylist.de_json,
    'promotion': Promotion.de_json,
    'album': Album.de_json,
    'playlist': Playlist.de_json,
    'chart-item': ChartItem.de_json,
    'play-context': PlayContext.de_json,
    'mix-link': MixLink.de_json,
}


@model
class BlockEntity(YandexMusicModel):
    """Класс, представляющий содержимое блока.

    Note:
        В зависимости от поля `type_`, в поле `data` будет объект соответствующего типа.

        Известные значения поля `type_`: `personal-playlist`, `promotion`, `album`, `playlist`, `chart-item`,
        `play-context`, `mix-link`.

    Attributes:
        id (:obj:`str`): Уникальный идентификатор содержимого.
        type (:obj:`str`): Тип содержимого.
        data (:obj:`yandex_music.GeneratedPlaylist` | :obj:`yandex_music.Promotion` | :obj:`yandex_music.Album` |
            :obj:`yandex_music.Playlist` | :obj:`yandex_music.ChartItem` | :obj:`yandex_music.PlayContext`  |
            :obj:`yandex_music.MixLink`): Содержимое.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    id: str
    type: str
    data: Union['GeneratedPlaylist', 'Promotion', 'Album', 'Playlist', 'ChartItem', 'PlayContext', 'MixLink']
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.id, self.type, self.data)

    @classmethod
    def de_json(cls, data: 'JSONType', client: 'ClientType') -> Optional['BlockEntity']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.BlockEntity`: Сущность (объект) блока.
        """
        if not cls.is_dict_model_data(data):
            return None

        cls_data = cls.cleanup_data(data, client)

        type_ = data.get('type')
        if isinstance(type_, str) and type_ in _TYPE_TO_DE_JSON_DEF:
            de_json_def = _TYPE_TO_DE_JSON_DEF[type_]
            cls_data['data'] = de_json_def(data.get('data'), client)

        return cls(client=client, **cls_data)  # type: ignore
