from typing import TYPE_CHECKING, Optional, List

from yandex_music import YandexMusicObject

if TYPE_CHECKING:
    from yandex_music import Client, Track, Chart


class ChartItem(YandexMusicObject):
    """Класс, представляющий трек в чарте.

    Attributes:
        track (:obj:`yandex_music.Track` | :obj:`None`): Трек.
        chart (:obj:`yandex_music.Chart` | :obj:`None`): Элемент чарта.
        client (:obj:`yandex_music.Client`): Клиент Yandex Music.

    Args:
        track (:obj:`yandex_music.Track` | :obj:`None`): Трек.
        chart (:obj:`yandex_music.Chart` | :obj:`None`): Элемент чарт.
        client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 track: Optional['Track'],
                 chart: Optional['Chart'],
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        super().handle_unknown_kwargs(self, **kwargs)

        self.track = track
        self.chart = chart

        self.client = client
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
        if not data:
            return None

        data = super(ChartItem, cls).de_json(data, client)
        from yandex_music import Chart, Track
        data['track'] = Track.de_json(data.get('track'), client)
        data['chart'] = Chart.de_json(data.get('chart'), client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data: dict, client: 'Client') -> List['ChartItem']:
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            client (:obj:`yandex_music.Client`, optional): Клиент Yandex Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.ChartItem`: Треки в чартах.
        """
        if not data:
            return []

        tracks = list()
        for track in data:
            tracks.append(cls.de_json(track, client))

        return tracks
