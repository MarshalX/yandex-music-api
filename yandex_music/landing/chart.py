from yandex_music import YandexMusicObject


class Chart(YandexMusicObject):
    def __init__(self,
                 position,
                 progress,
                 listeners,
                 shift,
                 track_id=None,
                 client=None,
                 **kwargs):
        self.position = position
        self.progress = progress
        self.listeners = listeners
        self.shift = shift

        self.track_id = track_id

        self.client = client
        self._id_attrs = (self.position, self.progress, self.listeners, self.shift, self.track_id)

    @classmethod
    def de_json(cls, data, client):
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
                Music.

        Returns:
            :obj:`yandex_music.Chart`: Объект класса :class:`yandex_music.Chart`.
        """

        if not data:
            return None

        data = super(Chart, cls).de_json(data, client)
        from yandex_music import TrackId
        data['track_id'] = TrackId.de_json(data.get('track_id'), client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data, client):
        """Десериализация списка объектов.

        Args:
            data (:obj:`list`): Список словарей с полями и значениями десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
                Music.

        Returns:
            :obj:`list` из :obj:`yandex_music.Chart`: Список объектов класса :class:`yandex_music.Chart`.
        """
        if not data:
            return []

        charts = list()
        for chart in data:
            charts.append(cls.de_json(chart, client))

        return charts
