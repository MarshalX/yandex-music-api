from typing import TYPE_CHECKING, Optional, List, Union

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client, BlockEntity, PersonalPlaylistsData, PlayContextsData


class Block(YandexMusicObject):
    """Класс, представляющий блок лендинга.

    Note:
        Известные значения поля `type_`: `personal-playlists`, `play-contexts`.

    Attributes:
        id_ (:obj:`str`): Уникальный идентификатор блока.
        type_ (:obj:`str`): Тип блока.
        type_for_from (:obj:`str`): Откуда получен блок (как к нему пришли).
        title (:obj:`str`): Заголовок.
        entities (:obj:`list` из :obj:`yandex_music.BlockEntity`): Содержимое блока (сущности, объекты).
        description (:obj:`str` | :obj:`None`): Описание.
        data (:obj:`yandex_music.PersonalPlaylistsData` | :obj:`yandex_music.PlayContextsData` | :obj:`None`):
            Дополнительные данные.
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.

    Args:
        id_ (:obj:`str`): Уникальный идентификатор блока.
        type_ (:obj:`str`): Тип блока.
        type_for_from (:obj:`str`): Откуда получен блок (как к нему пришли).
        title (:obj:`str`): Заголовок.
        entities (:obj:`list` из :obj:`yandex_music.BlockEntity`): Содержимое блока (сущности, объекты).
        description (:obj:`str`, optional): Описание.
        data (:obj:`yandex_music.PersonalPlaylistsData` | :obj:`yandex_music.PlayContextsData`, optional):
            Дополнительные данные.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 id_: str,
                 type_: str,
                 type_for_from: str,
                 title: str,
                 entities: List['BlockEntity'],
                 description: Optional[str] = None,
                 data: Optional[Union['PersonalPlaylistsData', 'PlayContextsData']] = None,
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        super().handle_unknown_kwargs(self, **kwargs)

        self.id = id_
        self.type = type_
        self.type_for_from = type_for_from
        self.title = title
        self.entities = entities

        self.description = description
        self.data = data

        self.client = client
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

        block_type = data.get('type_')
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
