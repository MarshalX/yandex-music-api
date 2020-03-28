from typing import TYPE_CHECKING

from yandex_music import YandexMusicObject, Playlist, ChartInfoMenu

if TYPE_CHECKING:
    from yandex_music import Client


class ChartInfo(YandexMusicObject):
    """Класс, представляющий чарт.

    Attributes:
        id (:obj:`str`): Уникальный идентификатор блока.
        type (:obj:`str`): Тип блока.
        type_for_from (:obj:`str`): Откуда получен блок (как к нему пришли).
        title (:obj:`str`): Заголовок.
        chart_description (:obj:`str`): Описание.
        menu (:obj:`dict`): Меню TODO.
        chart(:obj:`yandex_music.PlaylistId`): Плейлист.

    Args:
        id_ (:obj:`str`): Уникальный идентификатор блока.
        type_ (:obj:`str`): Тип блока.
        type_for_from (:obj:`str`): Откуда получен блок (как к нему пришли).
        title (:obj:`str`): Заголовок.
        chart_description (:obj:`str`): Описание.
        menu (:obj:`dict`): Меню TODO.
        chart(:obj:`yandex_music.PlaylistId`): Плейлист.
    """

    def __init__(self,
                 id_: str,
                 type_: str,
                 type_for_from: str,
                 title: str,
                 chart_description: str,
                 menu: 'ChartInfoMenu',
                 chart: 'Playlist'):
        self.id = id_
        self.type = type_
        self.type_for_from = type_for_from
        self.title = title
        self.chart_description = chart_description
        self.menu = menu
        self.chart = chart
        self._id_attrs = (id_,)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> 'ChartInfo':
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.ChartInfo`: Чарт.
        """
        if not data:
            return None

        data = super(ChartInfo, cls).de_json(data, client)
        data['chart'] = Playlist.de_json(data.get('chart'), client)
        data['menu'] = ChartInfoMenu.de_json(data.get('menu'), client)

        return cls(**data)
