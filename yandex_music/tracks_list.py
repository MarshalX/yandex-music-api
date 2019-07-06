from yandex_music import YandexMusicObject


class TracksList(YandexMusicObject):
    """Класс представляющий список треков.

    Attributes:
        uid (:obj:`int`): Уникальный идентификатор пользователя.
        revision (:obj:`int`): Актуальность данных TODO.
        tracks (:obj:`list` из :obj:`yandex_music.TrackShort`): Список треков.
        client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
                Music.

    Args:
        uid (:obj:`int`): Уникальный идентификатор пользователя.
        revision (:obj:`int`): Актуальность данных TODO.
        tracks (:obj:`list` из :obj:`yandex_music.TrackShort`): Список треков.
        client (:obj:`yandex_music.Client`, optional): Объект класса :class:`yandex_music.Client` представляющий клиент
            Yandex Music.
        **kwargs: Произвольные ключевые аргументы полученные от API.
    """

    def __init__(self,
                 uid,
                 revision,
                 tracks,
                 client=None,
                 **kwargs):
        self.uid = uid
        self.revision = revision
        self.tracks = tracks

        self.client = client

    def __getitem__(self, item):
        return self.tracks[item]

    def __iter__(self):
        return iter(self.tracks)

    @property
    def tracks_ids(self):
        """:obj:`list` из :obj:`str`: Список уникальных идентификаторов треков."""
        return [track.track_id for track in self.tracks]

    @classmethod
    def de_json(cls, data, client):
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
                Music.

        Returns:
            :obj:`yandex_music.TracksList`: Объект класса :class:`yandex_music.TracksList`.
        """
        if not data:
            return None

        data = super(TracksList, cls).de_json(data, client)
        from yandex_music import TrackShort
        data['tracks'] = TrackShort.de_list(data.get('tracks'), client)

        return cls(client=client, **data)
