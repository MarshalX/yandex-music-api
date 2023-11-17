from typing import TYPE_CHECKING, List, Optional

from yandex_music import YandexMusicObject
from yandex_music.utils import model

if TYPE_CHECKING:
    from yandex_music import Chart, Client, Track


@model
class ChartItem(YandexMusicObject):
    """Класс, представляющий трек в чарте.

    Attributes:
        track (:obj:`yandex_music.Track` | :obj:`None`): Трек.
        chart (:obj:`yandex_music.Chart` | :obj:`None`): Элемент чарт.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
    """

    track: Optional['Track']
    chart: Optional['Chart']
    client: Optional['Client'] = None

    def __post_init__(self) -> None:
        self._id_attrs = (self.track, self.chart)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['ChartItem']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`yandex_music.ChartItem`: Трек в чарте.
        """
        if not cls.is_valid_model_data(data):
            return None

        data = super(ChartItem, cls).de_json(data, client)
        from yandex_music import Chart, Track

        data['track'] = Track.de_json(data.get('track'), client)
        data['chart'] = Chart.de_json(data.get('chart'), client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data: list, client: 'Client') -> List['ChartItem']:
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.ChartItem`: Треки в чартах.
        """
        if not cls.is_valid_model_data(data, array=True):
            return []

        tracks = []
        for track in data:
            tracks.append(cls.de_json(track, client))

        return tracks
