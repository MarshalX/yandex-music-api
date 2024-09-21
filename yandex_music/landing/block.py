from typing import TYPE_CHECKING, List, Optional, Union

from yandex_music import JSONType, YandexMusicModel
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import BlockEntity, ClientType, PersonalPlaylistsData, PlayContextsData


@model
class Block(YandexMusicModel):
    """Класс, представляющий блок лендинга.

    Note:
        Известные значения поля `type_`: `personal-playlists`, `play-contexts`.

    Attributes:
        id (:obj:`str`): Уникальный идентификатор блока.
        type (:obj:`str`): Тип блока.
        type_for_from (:obj:`str`): Откуда получен блок (как к нему пришли).
        title (:obj:`str`): Заголовок.
        entities (:obj:`list` из :obj:`yandex_music.BlockEntity`): Содержимое блока (сущности, объекты).
        description (:obj:`str`, optional): Описание.
        data (:obj:`yandex_music.PersonalPlaylistsData` | :obj:`yandex_music.PlayContextsData`, optional):
            Дополнительные данные.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    id: str
    type: str
    type_for_from: str
    title: str
    entities: List['BlockEntity']
    description: Optional[str] = None
    data: Optional[Union['PersonalPlaylistsData', 'PlayContextsData']] = None
    client: Optional['ClientType'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.id, self.type, self.type_for_from, self.title, self.entities)

    def __getitem__(self, item: int) -> 'BlockEntity':
        return self.entities[item]

    @classmethod
    def de_json(cls, data: JSONType, client: 'ClientType') -> Optional['Block']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Block`: Блок лендинга.
        """
        if not cls.is_dict_model_data(data):
            return None

        data = cls.cleanup_data(data, client)
        from yandex_music import BlockEntity, PersonalPlaylistsData, PlayContextsData

        data['entities'] = BlockEntity.de_list(data.get('entities'), client)

        block_type = data.get('type')
        if block_type == 'personal-playlists':
            data['data'] = PersonalPlaylistsData.de_json(data.get('data'), client)
        elif block_type == 'play-contexts':
            data['data'] = PlayContextsData.de_json(data.get('data'), client)

        return cls(client=client, **data)
