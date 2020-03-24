from typing import TYPE_CHECKING

from yandex_music import YandexMusicObject, Playlist

if TYPE_CHECKING:
    from yandex_music import Client


class ChartInfo(YandexMusicObject):
    """Класс, представляющий чарт.

    Attributes:
        id_ (:obj:`str`): Уникальный идентификатор блока.
        type_ (:obj:`str`): Тип блока.
        type_for_from (:obj:`str`): Откуда получен блок (как к нему пришли).
        title (:obj:`str`): Заголовок.
        chart_description (:obj:`str`): Описание.
        menu (:obj:`dict`): Меню. TODO
        chart(:obj:`yandex_music.PlaylistId`): Плейлист.
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.

    Args:
        id_ (:obj:`str`): Уникальный идентификатор блока.
        type_ (:obj:`str`): Тип блока.
        type_for_from (:obj:`str`): Откуда получен блок (как к нему пришли).
        title (:obj:`str`): Заголовок.
        chart_description (:obj:`str`): Описание.
        menu (:obj:`dict`): Меню. TODO
        chart(:obj:`yandex_music.PlaylistId`): Плейлист.
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 id_: str,
                 type_: str,
                 type_for_from: str,
                 title: str,
                 chart_description: str,
                 menu: dict,
                 chart: 'Playlist',
                 client: 'Client',
                 **kwargs):
        self.id = id_
        self.type = type_
        self.type_for_from = type_for_from
        self.title = title
        self.chart_description = chart_description
        self.menu = menu
        self.chart = chart
        self.client = client

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> 'ChartInfo':
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.ChartInfo`: Чарт.
        """

        data = super(ChartInfo, cls).de_json(data, client)
        data['chart'] = Playlist.de_json(data.get('chart'), client)

        return cls(client=client, **data)
