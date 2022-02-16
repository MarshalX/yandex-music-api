from typing import TYPE_CHECKING, Optional, List, Union

from yandex_music import YandexMusicObject
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Client, BlockEntity, PersonalPlaylistsData, PlayContextsData


@model
class Block(YandexMusicObject):
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
    client: Optional['Client'] = None

    def __post_init__(self):
        self._id_attrs = (self.id, self.type, self.type_for_from, self.title, self.entities)

    def __getitem__(self, item: int) -> 'BlockEntity':
        return self.entities[item]

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['Block']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.Block`: Блок лендинга.
        """
        if not data:
            return None

        data = super(Block, cls).de_json(data, client)
        from yandex_music import BlockEntity, PlayContextsData, PersonalPlaylistsData

        data['entities'] = BlockEntity.de_list(data.get('entities'), client)

        block_type = data.get('type')
        if block_type == 'personal-playlists':
            data['data'] = PersonalPlaylistsData.de_json(data.get('data'), client)
        elif block_type == 'play-contexts':
            data['data'] = PlayContextsData.de_json(data.get('data'), client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data: dict, client: 'Client') -> List['Block']:
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.Block`: Блоки лендинга.
        """
        if not data:
            return []

        blocks = list()
        for block in data:
            blocks.append(cls.de_json(block, client))

        return blocks
