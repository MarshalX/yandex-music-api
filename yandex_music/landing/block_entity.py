from typing import TYPE_CHECKING, Optional, List, Union

from yandex_music import YandexMusicObject, Promotion, Album, Playlist, MixLink, PlayContext, ChartItem, \
    GeneratedPlaylist

if TYPE_CHECKING:
    from yandex_music import Client

de_json = {
    'personal-playlist': GeneratedPlaylist.de_json,
    'promotion': Promotion.de_json,
    'album': Album.de_json,
    'playlist': Playlist.de_json,
    'chart-item': ChartItem.de_json,
    'play-context': PlayContext.de_json,
    'mix-link': MixLink.de_json
}


class BlockEntity(YandexMusicObject):
    """Класс, представляющий содержимое блока.

    Note:
        В зависимости от поля `type_`, в поле `data` будет объект соответствующего типа.

        Известные значения поля `type_`: `personal-playlist`, `promotion`, `album`, `playlist`, `chart-item`,
        `play-context`, `mix-link`.

    Attributes:
        id_ (:obj:`str`): Уникальный идентификатор содержимого.
        type_ (:obj:`str`): Тип содержимого.
        data (:obj:`yandex_music.GeneratedPlaylist` | :obj:`yandex_music.Promotion` | :obj:`yandex_music.Album` |
            :obj:`yandex_music.Playlist` | :obj:`yandex_music.ChartItem` | :obj:`yandex_music.PlayContext`  |
            :obj:`yandex_music.MixLink`): Содержимое.
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.

    Args:
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 id_: str,
                 type_: str,
                 data: Optional[Union['GeneratedPlaylist', 'Promotion', 'Album',
                                      'Playlist', 'ChartItem', 'PlayContext', 'MixLink']],
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        self.id = id_
        self.type = type_
        self.data = data

        self.client = client
        self._id_attrs = (self.id, self.type, self.data)

        super().handle_unknown_kwargs(self, **kwargs)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['BlockEntity']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.BlockEntity`: Сущность (объект) блока.
        """
        if not data:
            return None

        data = super(BlockEntity, cls).de_json(data, client)
        data['data'] = de_json.get(data.get('type_'))(data.get('data'), client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data: dict, client: 'Client') -> List['BlockEntity']:
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.BlockEntity`: Содержимое блока.
        """
        if not data:
            return []

        entities = list()
        for entity in data:
            entities.append(cls.de_json(entity, client))

        return entities
